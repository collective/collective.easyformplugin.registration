# -*- coding: utf-8 -*-
from collective.easyformplugin.registration import _
from plone.app.event.base import default_timezone
from plone.app.z3cform.widget import DatetimeFieldWidget
from plone.autoform import directives
from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel import model
from plone.supermodel.directives import fieldset
from zope import schema
from zope.interface import provider


@provider(IFormFieldProvider)
class IRegistrationForm(model.Schema):
    """Behavior interface to make a EasyForm type support registration form.
    """

    is_registration_form = schema.Bool(
        title=_(u"label_is_registration_form", default=u"Registration form"),
        description=_(
            "help_is_registration_form",
            default=u"Select if this form is a registration form. "
            u"If selected, will be created a new form action (registrants) and"
            u" a new hidden field (waiting_list). If one of these two defaults"
            u" is missing, the registration form can't work properly.",
        ),
        required=False
    )

    max_attendees = schema.Int(
        title=_(u"label_max_attendees", default=u"Max attendees"),
        description=_(
            "help_max_attendees",
            default=u"Set a maximum number of attendees for this registration"
            u" form. Leave empty for unlimited.",
        ),
        required=False,
    )

    waiting_list_size = schema.Int(
        title=_(u"label_waiting_list_size", default=u"Waiting list size"),
        description=_(
            "help_waiting_list_size",
            default=u"Set a number of available seats in waiting list."
            u" Leave empty for disable the waiting list.",
        ),
        required=False,
    )

    show_seats_left = schema.Bool(
        title=_(u"label_show_seats_left", default=u"Show seats left"),
        description=_(
            "help_show_seats_left",
            default=u"Allows to show in the subscription page how many seats "
            u"are still available. Waiting list seats are not counted.",
        ),
        required=False
    )

    open_date = schema.Datetime(
        title=_(u"label_subscription_open_date", default=u"Open date"),
        description=_(
            u"help_subscription_open_date",
            default=u"Date and Time, when the registration form opens.",
        ),
        required=False,
        # defaultFactory=default_open_date,
    )
    directives.widget(
        "open_date", DatetimeFieldWidget, default_timezone=default_timezone
    )

    close_date = schema.Datetime(
        title=_(u"label_subscription_close_date", default=u"Close date"),
        description=_(
            u"help_subscription_close_date",
            default=u"Date and Time, when the registration form closes.",
        ),
        required=False,
        # defaultFactory=default_close_date,
    )
    directives.widget(
        "close_date", DatetimeFieldWidget, default_timezone=default_timezone
    )

    fieldset(
        "Registration",
        label=_(u"Registration"),
        fields=[
            "is_registration_form",
            "max_attendees",
            "waiting_list_size",
            "show_seats_left",
            "open_date",
            "close_date",
        ],
    )
