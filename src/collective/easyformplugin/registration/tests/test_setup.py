# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from collective.easyformplugin.registration.testing import (
    COLLECTIVE_EASYFORMPLUGIN_REGISTRATION_INTEGRATION_TESTING,
)
from plone import api
from plone.app.testing import setRoles, TEST_USER_ID

import unittest

try:
    from Products.CMFPlone.utils import get_installer
except ImportError:
    get_installer = None


class TestSetup(unittest.TestCase):
    """Test that collective.easyformplugin.registration is properly installed."""

    layer = COLLECTIVE_EASYFORMPLUGIN_REGISTRATION_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer["portal"]
        if get_installer:
            self.installer = get_installer(self.portal, self.layer["request"])
        else:
            self.installer = api.portal.get_tool("portal_quickinstaller")

    def test_product_installed(self):
        """Test if collective.easyformplugin.registration is installed."""
        self.assertTrue(
            self.installer.isProductInstalled("collective.easyformplugin.registration")
        )

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
        if get_installer:
            self.installer = get_installer(self.portal, self.layer["request"])
        else:
            self.installer = api.portal.get_tool("portal_quickinstaller")
        roles_before = api.user.get_roles(TEST_USER_ID)
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        self.installer.uninstallProducts(["collective.easyformplugin.registration"])
        setRoles(self.portal, TEST_USER_ID, roles_before)

    def test_product_uninstalled(self):
        """Test if collective.easyformplugin.registration is cleanly uninstalled."""
        self.assertFalse(
            self.installer.isProductInstalled("collective.easyformplugin.registration")
        )

    def test_browserlayer_removed(self):
        """Test that ICollectiveEASYFORMPLUGIN_REGISTRATIONLayer is removed."""
        from collective.easyformplugin.registration.interfaces import (
            ICollectiveEasyFormpluginRegistrationLayer,
        )
        from plone.browserlayer import utils

        self.assertNotIn(
            ICollectiveEasyFormpluginRegistrationLayer, utils.registered_layers()
        )
