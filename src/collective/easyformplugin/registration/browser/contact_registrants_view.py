# -*- coding: utf-8 -*-
from collective.easyform.api import get_actions
from collective.easyformplugin.registration import _
from collective.easyformplugin.registration.interfaces import IRegistrantData
from email.mime.text import MIMEText
from Products.CMFPlone import PloneMessageFactory as pmf
from plone import api
from plone.registry.interfaces import IRegistry
from plone.supermodel import model
from plone.z3cform import layout
from Products.CMFPlone.interfaces.controlpanel import IMailSchema
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from smtplib import SMTPException
from z3c.form import button
from z3c.form import field
from z3c.form import form
from z3c.form.browser.checkbox import CheckBoxFieldWidget
from zope import schema
from zope.component import getUtility
from zope.schema import getFieldsInOrder

import logging
import pkg_resources

logger = logging.getLogger(__name__)


class IContactRegistrantsForm(model.Schema):
    subject = schema.TextLine(title=_(u'Subject'), required=True)
    message = schema.Text(title=_(u'Message'), required=True)

    registrants = schema.Tuple(
        title=_(u'Registrants'),
        description=_(
            u'List of registered people that compiled email fields '
            u'(could be one of these fields: email, e-mail, replyto).'
        ),
        required=False,
        default=(),
        missing_value=(),
        value_type=schema.Choice(
            source='collective.easyformplugin.registration.registrants'
        ),
    )
    waiting_list = schema.Tuple(
        title=_(u'Waiting list'),
        description=_(
            u'List of people in waiting list that compiled email fields '
            u'(could be one of these fields: email, e-mail, replyto).'
        ),
        required=False,
        default=(),
        missing_value=(),
        value_type=schema.Choice(
            source='collective.easyformplugin.registration.waiting_list'
        ),
    )


class ContactRegistrantsForm(form.Form):
    """
    Contact registrants form
    """

    ignoreContext = True
    css_class = 'contact-registrants'
    fields = field.Fields(IContactRegistrantsForm)

    fields['registrants'].widgetFactory = CheckBoxFieldWidget
    fields['waiting_list'].widgetFactory = CheckBoxFieldWidget

    @button.buttonAndHandler(_(u'Submit'), name='submit')
    def handleSubmit(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return
        registrants = data.get('registrants', [])
        waiting_list = data.get('waiting_list', [])
        if not registrants and not waiting_list:
            api.portal.show_message(
                message=_(
                    'contact_recipients_error',
                    default=u'You need to select at least one recipient from'
                    u' registrants or waiting_list list.',
                ),
                request=self.request,
                type='error',
            )
            return
        email_addresses = self.extract_recipients(registrants, waiting_list)
        if isinstance(email_addresses, str):
            api.portal.show_message(
                message=email_addresses, request=self.request, type='error'
            )
            return
        try:
            self.send_message(data=data, email_addresses=email_addresses)
            api.portal.show_message(
                message=_('contact_recipients_sent', u'Emails sent.'),
                request=self.request,
            )
            self.request.response.redirect(self.nextURL())
        except (SMTPException, RuntimeError) as e:
            logger.exception(e)
            plone_utils = api.portal.get_tool(name='plone_utils')
            exception = plone_utils.exceptionString()
            message = pmf(
                u'Unable to send mail: ${exception}',
                mapping={u'exception': exception},
            )
            api.portal.show_message(
                message=message, request=self.request, type='error'
            )

    @button.buttonAndHandler(_(u'Reset'), name='reset')
    def handleReset(self, action):
        self.request.response.redirect(self.nextURL())

    def nextURL(self):
        return self.context.absolute_url()

    def extract_recipients(self, registrants, waiting_list):
        emails = []
        registrants_action = None
        for name, action in getFieldsInOrder(get_actions(self.context)):
            if IRegistrantData.providedBy(action) and action.required:
                registrants_action = action
        if not registrants_action:
            return _(
                'contact_registrants_action_not_found',
                default=u'Unable to send messages. Action not found in Form.',
            )
        for registrant in registrants_action._storage.values():
            if (
                registrant.get('id') in registrants
                or registrant.get('id') in waiting_list
            ):
                email = (
                    registrant.get('email', '')
                    or registrant.get('e-mail', '')
                    or registrant.get('replyto', '')
                )
                emails.append(email)
        return set(emails)

    def generate_mail(self, variables, encoding='utf-8'):
        template = api.content.get_view(
            name='contact-registrants-email',
            context=self.context,
            request=self.request,
        )
        return template(self.context, **variables).encode(encoding)

    def send_message(self, data, email_addresses):
        subject = data.get('subject')

        registry = getUtility(IRegistry)
        mail_settings = registry.forInterface(IMailSchema, prefix='plone')
        send_to_address = mail_settings.email_from_address
        from_address = mail_settings.email_from_address
        registry = getUtility(IRegistry)
        encoding = registry.get('plone.email_charset', 'utf-8')
        host = api.portal.get_tool(name='MailHost')

        message = self.generate_mail(data, encoding)
        message = MIMEText(message, 'plain', encoding)
        for send_to_address in email_addresses:
            # This actually sends out the mail
            host.send(
                message,
                send_to_address,
                from_address,
                subject=subject,
                charset=encoding,
            )

    def get_package_version(self):
        return pkg_resources.get_distribution(
            "collective.easyformplugin.registration"
        ).version


ContactRegistrantsView = layout.wrap_form(
    ContactRegistrantsForm,
    index=ViewPageTemplateFile('contact_registrants_view.pt'),
)
