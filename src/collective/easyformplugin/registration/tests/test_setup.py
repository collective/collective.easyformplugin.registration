"""Setup tests for this package."""

from collective.easyformplugin.registration.testing import (
    COLLECTIVE_EASYFORMPLUGIN_REGISTRATION_INTEGRATION_TESTING,
)
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from Products.CMFPlone.utils import get_installer

import unittest


PRODUCT_NAME = "collective.easyformplugin.registration"


class TestSetup(unittest.TestCase):
    """Test that collective.easyformplugin.registration is properly installed."""

    layer = COLLECTIVE_EASYFORMPLUGIN_REGISTRATION_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer["portal"]
        self.installer = get_installer(self.portal, self.layer["request"])

    def test_product_installed(self):
        """Test if collective.easyformplugin.registration is installed."""
        self.assertTrue(self.installer.is_product_installed(PRODUCT_NAME))

    def test_browserlayer(self):
        """Test that ICollectiveEASYFORMPLUGIN_REGISTRATIONLayer is registered."""
        from collective.easyformplugin.registration.interfaces import (
            ICollectiveEasyFormpluginRegistrationLayer,
        )
        from plone.browserlayer import utils

        self.assertIn(
            ICollectiveEasyFormpluginRegistrationLayer, utils.registered_layers()
        )


class TestUninstall(unittest.TestCase):
    layer = COLLECTIVE_EASYFORMPLUGIN_REGISTRATION_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        self.installer = get_installer(self.portal, self.layer["request"])
        roles_before = api.user.get_roles(TEST_USER_ID)
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        self.installer.uninstall_product(PRODUCT_NAME)
        setRoles(self.portal, TEST_USER_ID, roles_before)

    def test_product_uninstalled(self):
        """Test if collective.easyformplugin.registration is cleanly uninstalled."""
        self.assertFalse(self.installer.is_product_installed(PRODUCT_NAME))

    def test_browserlayer_removed(self):
        """Test that ICollectiveEASYFORMPLUGIN_REGISTRATIONLayer is removed."""
        from collective.easyformplugin.registration.interfaces import (
            ICollectiveEasyFormpluginRegistrationLayer,
        )
        from plone.browserlayer import utils

        self.assertNotIn(
            ICollectiveEasyFormpluginRegistrationLayer, utils.registered_layers()
        )
