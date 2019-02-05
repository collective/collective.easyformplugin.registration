# -*- coding: utf-8 -*-
from collective.easyform.api import filter_fields
from collective.easyform.api import get_actions
from collective.easyform.api import get_expression
from collective.easyform.api import set_actions
from collective.easyform.browser.view import EasyFormForm
from collective.easyform.interfaces import IActionExtender
from collective.easyform.interfaces import IEasyFormForm
from collective.easyformplugin.registration import _
from collective.easyformplugin.registration.interfaces import IRegistrantData
from datetime import datetime
from plone import api
from plone.app.event.base import default_timezone
from plone.memoize.view import memoize
from plone.z3cform import layout
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from z3c.form.interfaces import HIDDEN_MODE
from zope.interface import implementer
from zope.schema import getFieldsInOrder

import pytz


@implementer(IEasyFormForm)
class RegistrationFormForm(EasyFormForm):
    """
    Registration Form
    """

    form_template = ViewPageTemplateFile('registration_form.pt')

    def extractData(self):
        """
        workaround: waiting_list is an hiddend field with a default value,
        but z3cform gives it a strange value in the form
        """
        data, errors = super(RegistrationFormForm, self).extractData()
        field_id = 'waiting_list'
        if self.request.form.get('form.widgets.waiting_list', '') == [
            u'selected',
            u'unselected',
        ]:
            data[field_id] = False
        return data, errors

    def setThanksFields(self, fields, data):
        """
        don't show hiddend fields in thank you page
        """
        omit = filter_fields(self.context, self.schema, data, omit=True)
        new_fields = []
        for fname, field in fields.items():
            if field.mode == HIDDEN_MODE:
                continue
            new_fields.append(field)
        fields = fields.__class__(*new_fields)
        if omit:
            fields = fields.omit(*omit)

        return fields

    def processActions(self, fields):
        # get a list of adapters with no duplicates, retaining order
        actions = getFieldsInOrder(get_actions(self.context))
        for name, action in actions:
            if not action.required:
                continue
            # Now, see if we should execute it.
            # Check to see if execCondition exists and has contents
            execCondition = IActionExtender(action).execCondition
            if execCondition:
                doit = get_expression(self.context, execCondition)
            else:
                doit = True
            if doit and hasattr(action, 'onSuccess'):
                if IRegistrantData.providedBy(action):
                    result = action.onSuccess(
                        fields,
                        self.request,
                        max_attendees=getattr(self.context, 'max_attendees', 0),
                        waiting_list_size=getattr(
                            self.context, 'waiting_list_size', 0
                        ),
                    )
                else:
                    result = action.onSuccess(fields, self.request)
                if isinstance(result, dict) and len(result):
                    return result

    @memoize
    def get_form_status(self):
        res = {'active': True}
        dates_status_error = self.get_dates_status_error()
        if dates_status_error:
            res['active'] = False
            res.update(dates_status_error)
            return res
        max_attendees = getattr(self.context, 'max_attendees', 0)
        waiting_list_size = getattr(self.context, 'waiting_list_size', 0)
        if not max_attendees:
            # no limit
            return res
        registrants_data = self.registrants_data
        if registrants_data.has_reached_subscriptions_limit(
            max_attendees=max_attendees, waiting_list_size=waiting_list_size
        ):
            if registrants_data.waiting_list_is_open(
                max_attendees=max_attendees, waiting_list_size=waiting_list_size
            ):
                res['status_message'] = self.set_status_message(
                    message=_(
                        'message_waiting_list_open',
                        default=u'You can subscribe anyway and enter'
                        u' to a waiting list. '
                        u'We will contact you in case some '
                        u'participants will cancel their subscription.',
                    ),
                    strong_message=_(
                        'message_waiting_list_open_strong',
                        default=u'Attendees limit reached.',
                    ),
                    type='warning',
                )
            else:
                res['active'] = False
                res['status_message'] = self.set_status_message(
                    message=_(
                        'message_attendees_limit_reached',
                        default=u'Attendees limit reached.',
                    ),
                    type='error',
                )
        return res

    def get_dates_status_error(self):
        open_date = getattr(self.context, 'open_date', None)
        close_date = getattr(self.context, 'close_date', None)
        now = datetime.now(pytz.timezone(default_timezone()))
        res = {}
        if not open_date and not close_date:
            return res
        if not open_date:
            if now > close_date:
                res['status_message'] = self.close_past_msg(close_date)
            return res
        elif not close_date:
            if now < open_date:
                res['status_message'] = self.open_future_msg(open_date)
            return res
        if not open_date < now < close_date:
            # too early or too late
            res['active'] = False
            if open_date > now:
                res['status_message'] = self.open_future_msg(open_date)
            elif close_date < now:
                res['status_message'] = self.close_past_msg(close_date)
        return res

    def open_future_msg(self, date):
        return self.set_status_message(
            message=_(
                'message_open_date_future',
                default=u'Registration opening on ${date} at ${hour}.',
                mapping={
                    'date': api.portal.get_localized_time(datetime=date),
                    'hour': date.time().strftime('%H:%M'),
                },
            ),
            type='warning',
        )

    def close_past_msg(self, date):
        return self.set_status_message(
            message=_(
                'message_close_date_past',
                default=u'Registration ended on ${date} at ${hour}.',
                mapping={
                    'date': api.portal.get_localized_time(datetime=date),
                    'hour': date.time().strftime('%H:%M'),
                },
            ),
            type='error',
        )

    def set_status_message(self, message, type, strong_message=''):
        if not strong_message:
            strong_message = _(
                'registration_form_error',
                default=u'You can\'t subscribe to this form.',
            )
        return {
            'type': type,
            'message': message,
            'strong_message': strong_message,
        }

    @property
    def available_seats(self):
        max_attendees = getattr(self.context, 'max_attendees', None)
        data = self.registrants_data
        registrants = 0
        for registrant in data._storage.values():
            if not registrant.get('waiting_list', False):
                registrants += 1
        return max_attendees - registrants

    @property
    def registrants_data(self):
        for name, action in getFieldsInOrder(get_actions(self.context)):
            if IRegistrantData.providedBy(action) and action.required:
                return action


RegistrationFormView = layout.wrap_form(RegistrationFormForm)
