# -*- coding: utf-8 -*-
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.testing import (
    applyProfile,
    FunctionalTesting,
    IntegrationTesting,
    PloneSandboxLayer,
)

import collective.easyform
import collective.easyformplugin.registration


class CollectiveEasyFormpluginRegistrationLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        self.loadZCML(package=collective.easyformplugin.registration)
        self.loadZCML(package=collective.easyform)

    def setUpPloneSite(self, portal):
        applyProfile(portal, "collective.easyformplugin.registration:default")


COLLECTIVE_EASYFORMPLUGIN_REGISTRATION_FIXTURE = (
    CollectiveEasyFormpluginRegistrationLayer()
)


COLLECTIVE_EASYFORMPLUGIN_REGISTRATION_INTEGRATION_TESTING = IntegrationTesting(
    bases=(COLLECTIVE_EASYFORMPLUGIN_REGISTRATION_FIXTURE,),
    name="CollectiveEasyFormpluginRegistrationLayer:IntegrationTesting",
)


COLLECTIVE_EASYFORMPLUGIN_REGISTRATION_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(COLLECTIVE_EASYFORMPLUGIN_REGISTRATION_FIXTURE,),
    name="CollectiveEasyFormpluginRegistrationLayer:FunctionalTesting",
)
