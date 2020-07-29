# -*- coding: utf-8 -*-
from collective.easyformplugin.registration.interfaces import (
    IEasyFormRegistrationEnabled,
)
from lxml import etree
from plone.supermodel import loadString
from Products.CMFPlone.utils import safe_unicode
from Products.Five.utilities.marker import erase, mark

import os

FIELDS_DEFAULT_FILENAME = "fields_default.xml"
ACTIONS_DEFAULT_FILENAME = "actions_default.xml"


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
    if getattr(context, "is_registration_form", False):
        mark(context, IEasyFormRegistrationEnabled)
        updateActionsSchema(context)
    else:
        erase(context, IEasyFormRegistrationEnabled)
    context.reindexObject(idxs=["object_provides"])


def readSchemaFromFile(filename):
    this_path = os.path.dirname(__file__)
    with open(os.path.join(this_path, "default_schemata", filename)) as f:
        return safe_unicode(f.read())


def updateActionsSchema(context):
    """
    Add default actions only if not present.
    """
    schema = readSchemaFromFile(ACTIONS_DEFAULT_FILENAME)
    register_xml = etree.fromstring(schema)
    form_xml = etree.fromstring(context.actions_model)
    action_names = loadString(context.actions_model).schema.names()
    new_fields = register_xml.findall(
        ".//{http://namespaces.plone.org/supermodel/schema}field"
    )
    old_schema = form_xml.findall(
        ".//{http://namespaces.plone.org/supermodel/schema}schema"
    )[0]
    for new_field in new_fields:
        if new_field.get("name") not in action_names:
            old_schema.append(new_field)
    context.actions_model = etree.tostring(form_xml)


def updateFieldsSchema(context):
    """
    Add waiting list field, if waiting list is set and not present.
    """
    schema = readSchemaFromFile(FIELDS_DEFAULT_FILENAME)
    register_xml = etree.fromstring(schema)
    form_xml = etree.fromstring(context.fields_model)
    fields_names = loadString(context.fields_model).schema.names()
    new_fields = register_xml.findall(
        ".//{http://namespaces.plone.org/supermodel/schema}field"
    )
    old_schema = form_xml.findall(
        ".//{http://namespaces.plone.org/supermodel/schema}schema"
    )[0]
    for new_field in new_fields:
        if new_field.get("name") not in fields_names:
            old_schema.append(new_field)
    context.fields_model = etree.tostring(form_xml)
