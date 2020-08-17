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

    """Own Interface for registrants  """
    # no extra fields so far.

