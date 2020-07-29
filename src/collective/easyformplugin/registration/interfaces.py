# -*- coding: utf-8 -*-
from collective.easyform.interfaces import ISaveData
from collective.easyformplugin.registration import _
from plone.autoform import directives
from plone.z3cform.interfaces import IFormWrapper
from z3c.form.browser.checkbox import CheckBoxFieldWidget
from zope.interface import Interface
from zope.publisher.interfaces.browser import IDefaultBrowserLayer

import zope.interface
import zope.schema.interfaces


class ICollectiveEasyFormpluginRegistrationLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""


class IEasyFormRegistrationEnabled(Interface):
    """ Marker interface set when a form is marked as Registration Form. """


class IRegistrantDataFormWrapper(IFormWrapper):
    pass


class IRegistrantData(ISaveData):

    """ """

    showFields = zope.schema.List(
        title=_(u"label_savefields_text", default=u"Saved Fields"),
        description=_(
            u"help_savefields_text",
            default=u"Pick the fields whose inputs you'd like to include in "
            u"the saved data. If empty, all fields will be saved.",
        ),
        unique=True,
        required=False,
        value_type=zope.schema.Choice(vocabulary="easyform.Fields"),
    )
    directives.widget(ExtraData=CheckBoxFieldWidget)
    ExtraData = zope.schema.List(
        title=_(u"label_savedataextra_text", default="Extra Data"),
        description=_(
            u"help_savedataextra_text",
            default=u"Pick any extra data you'd like saved with the form " u"input.",
        ),
        unique=True,
        value_type=zope.schema.Choice(vocabulary="easyform.ExtraDataDL"),
    )
    DownloadFormat = zope.schema.Choice(
        title=_(u"label_downloadformat_text", default=u"Download Format"),
        default=u"csv",
        vocabulary="easyform.FormatDL",
    )
    UseColumnNames = zope.schema.Bool(
        title=_(u"label_usecolumnnames_text", default=u"Include Column Names"),
        description=_(
            u"help_usecolumnnames_text",
            default=u"Do you wish to have column names on the first line of "
            u"downloaded input?",
        ),
        required=False,
    )
