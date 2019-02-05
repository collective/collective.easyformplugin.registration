# -*- coding: utf-8 -*-
from collective.easyform.api import get_actions
from collective.easyformplugin.registration.interfaces import IRegistrantData
from zope.interface import provider
from zope.schema import getFieldsInOrder
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


@provider(IVocabularyFactory)
def registrants_vocabulary_factory(context):
    registrants_action = None
    for name, action in getFieldsInOrder(get_actions(context)):
        if IRegistrantData.providedBy(action) and action.required:
            registrants_action = action
    if not registrants_action:
        return SimpleVocabulary([])
    terms = [
        extract_registrant_infos(x)
        for x in registrants_action._storage.values()
        if not x.get('waiting_list', False)
    ]
    return SimpleVocabulary(terms)


@provider(IVocabularyFactory)
def waiting_list_vocabulary_factory(context):
    registrants_action = None
    for name, action in getFieldsInOrder(get_actions(context)):
        if IRegistrantData.providedBy(action) and action.required:
            registrants_action = action
    if not registrants_action:
        return SimpleVocabulary([])
    terms = [
        extract_registrant_infos(x)
        for x in registrants_action._storage.values()
        if x.get('waiting_list', False)
    ]
    return SimpleVocabulary(terms)


def extract_registrant_infos(registrant):
    fullname = registrant.get('fullname', '')
    name = registrant.get('name', '')
    surname = registrant.get('surname', '')
    email = registrant.get('email', '') or registrant.get('replyto', '')
    registrant_name = email
    if fullname:
        registrant_name = fullname
    elif surname and name:
        registrant_name = "{0} {1}".format(surname, name)
    return SimpleTerm(
        value=registrant.get('id', ''),
        token=registrant.get('id', ''),
        title=registrant_name,
    )

