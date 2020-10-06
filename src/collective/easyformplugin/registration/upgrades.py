# -*- coding: utf-8 -*-
from plone import api
from zope.component import queryUtility
from plone.dexterity.interfaces import IDexterityFTI

import logging

logger = logging.getLogger(__name__)

BEHAVIOR_NAME_MAPPING = {
    "plone.app.content.interfaces.INameFromTitle": "plone.namefromtitle",
    "plone.app.dexterity.behaviors.discussion.IAllowDiscussion": "plone.allowdiscussion",
    "plone.app.dexterity.behaviors.exclfromnav.IExcludeFromNavigation": "plone.excludefromnavigation",
    "plone.app.dexterity.behaviors.metadata.IDublinCore": "plone.dublincore",
    "collective.easyformplugin.registration.behavior.IRegistrationForm": "easyformplugin.registration",
}


def rename_behavior_interface(context=None):
    """Rename iface name to the short name """
    pt = api.portal.get_tool("portal_types")
    for old_behavior_name, short_name in BEHAVIOR_NAME_MAPPING.items():
        print(old_behavior_name, short_name)
    for _type in pt.objectIds():
        fti = queryUtility(IDexterityFTI, name=_type)

        for old_behavior_name, short_name in BEHAVIOR_NAME_MAPPING.items():
            if fti and old_behavior_name in fti.behaviors:
                new_fti = [
                    currentbehavior
                    for currentbehavior in fti.behaviors
                    if currentbehavior != old_behavior_name
                ]
                new_fti.append(short_name)
                fti.behaviors = tuple(new_fti)
                logger.info("Migrated behavior of {} type".format(_type))
