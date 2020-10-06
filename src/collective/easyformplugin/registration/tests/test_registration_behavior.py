# -*- coding: utf-8 -*-
from plone.app.testing import setRoles
from plone.app.testing import SITE_OWNER_NAME
from plone.app.testing import SITE_OWNER_PASSWORD
from plone.app.testing import TEST_USER_ID
from plone.dexterity.fti import DexterityFTI
from plone.testing.zope import Browser
from collective.easyformplugin.registration.behavior import IRegistrationForm
from collective.easyformplugin.registration.testing import (
    COLLECTIVE_EASYFORMPLUGIN_REGISTRATION_FUNCTIONAL_TESTING,
)
import unittest


class RegistrationFormBase:
    # subclass here
    _behaviors = None
    _portal_type = None

    def _setupFTI(self):
        fti = DexterityFTI(self._portal_type)
        self.portal.portal_types._setObject(self._portal_type, fti)
        fti.klass = "plone.dexterity.content.Item"
        fti.behaviors = self._behaviors


class EasyFormRegistrationBehaviorFunctionalTest(
    RegistrationFormBase, unittest.TestCase
):
    """ basic use cases and tests for richtext behavior"""

    layer = COLLECTIVE_EASYFORMPLUGIN_REGISTRATION_FUNCTIONAL_TESTING

    _behaviors = ("easyformplugin.registration",)
    _portal_type = "TestEasyForm"

    def setUp(self):
        app = self.layer["app"]
        self.portal = self.layer["portal"]
        self.portal_url = self.portal.absolute_url()
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        self._setupFTI()
        self.portal.invokeFactory(self._portal_type, "easyform1")
        setRoles(self.portal, TEST_USER_ID, ["Member"])

        import transaction
        transaction.commit()

        # Set up browser
        self.browser = Browser(app)
        self.browser.handleErrors = False
        self.browser.addHeader(
            "Authorization",
            "Basic {0}:{1}".format(
                SITE_OWNER_NAME,
                SITE_OWNER_PASSWORD,
            ),
        )

    def test_easyform_registration_in_edit_form(self):
        self.browser.open(self.portal_url + "/easyform1/edit")
        self.assertTrue("fieldset-registration" in self.browser.contents)

    def test_easyform_registration_behavior(self):
        IRegistrationForm.providedBy(self.portal.easyform1)
