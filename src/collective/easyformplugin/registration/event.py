# -*- coding: utf-8 -*-
from collective.easyformplugin.registration.interfaces import (
    IEasyFormRegistrationEnabled,
)
from lxml import etree
from plone.supermodel import loadString
from Products.CMFPlone.utils import safe_unicode
from Products.Five.utilities.marker import erase
from Products.Five.utilities.marker import mark

import os


this_path = os.path.dirname(__file__)

FIELDS_DEFAULT = safe_unicode(
    open(
        os.path.join(this_path, "default_schemata", "fields_default.xml")
    ).read()
)

ACTIONS_DEFAULT = safe_unicode(
    open(
        os.path.join(this_path, "default_schemata", "actions_default.xml")
    ).read()
)


def handle_add_form(obj, event):
    set_actions(obj)
    updateFieldsSchema(obj)


def handle_edit_form(obj, event):
    set_actions(obj)
    updateFieldsSchema(obj)


def set_actions(context):
    """
    Set registration actions
    """
    if getattr(context, 'is_registration_form', False):
        mark(context, IEasyFormRegistrationEnabled)
        updateActionsSchema(context)
    else:
        erase(context, IEasyFormRegistrationEnabled)
    context.reindexObject(idxs=['object_provides'])


def updateActionsSchema(context):
    """
    Add default actions only if not present.
    """
    register_xml = etree.fromstring(ACTIONS_DEFAULT)
    form_xml = etree.fromstring(context.actions_model)
    action_names = loadString(context.actions_model).schema.names()
    new_fields = register_xml.findall(
        './/{http://namespaces.plone.org/supermodel/schema}field'
    )
    old_schema = form_xml.findall(
        './/{http://namespaces.plone.org/supermodel/schema}schema'
    )[0]
    for new_field in new_fields:
        if new_field.get('name') not in action_names:
            old_schema.append(new_field)
    context.actions_model = etree.tostring(form_xml)


def updateFieldsSchema(context):
    """
    Add waiting list field, if waiting list is set and not present.
    """
    register_xml = etree.fromstring(FIELDS_DEFAULT)
    form_xml = etree.fromstring(context.fields_model)
    fields_names = loadString(context.fields_model).schema.names()
    new_fields = register_xml.findall(
        './/{http://namespaces.plone.org/supermodel/schema}field'
    )
    old_schema = form_xml.findall(
        './/{http://namespaces.plone.org/supermodel/schema}schema'
    )[0]
    for new_field in new_fields:
        if new_field.get('name') not in fields_names:
            old_schema.append(new_field)
    context.fields_model = etree.tostring(form_xml)
