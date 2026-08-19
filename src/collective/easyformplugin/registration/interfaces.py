from collective.easyform.interfaces import ISaveData
from plone.z3cform.interfaces import IFormWrapper
from zope.interface import Interface
from zope.publisher.interfaces.browser import IDefaultBrowserLayer


class ICollectiveEasyFormpluginRegistrationLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""


class IEasyFormRegistrationEnabled(Interface):
    """Marker interface set when a form is marked as Registration Form."""


class IRegistrantDataFormWrapper(IFormWrapper):
    pass


class IRegistrantData(ISaveData):
    """Own Interface for registrants"""

    # no extra fields so far.
