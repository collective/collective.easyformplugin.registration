# -*- coding: utf-8 -*-
from BTrees.LOBTree import LOBTree as SavedDataBTree
from collective.easyform import easyformMessageFactory as _
from collective.easyform.actions import ActionFactory, SaveData
from collective.easyform.api import get_context
from collective.easyformplugin.registration.interfaces import IRegistrantData
from DateTime import DateTime
from logging import getLogger
from plone.supermodel.exportimport import BaseHandler
from zope.interface import implementer

logger = getLogger("collective.easyform")


@implementer(IRegistrantData)
class RegistrantData(SaveData):
    __doc__ = IRegistrantData.__doc__

    def __init__(self, **kw):
        for i, f in IRegistrantData.namesAndDescriptions():
            setattr(self, i, kw.pop(i, f.default))
        super(RegistrantData, self).__init__(**kw)

    def onSuccess(self, fields, request, max_attendees, waiting_list_size):
        """
        saves data. Ignore waiting_list value given from data.
        """
        if self.has_reached_limit(
            max_attendees=max_attendees, waiting_list_size=waiting_list_size
        ):
            return {"error": "Limit reached"}
        data = {}
        showFields = getattr(self, "showFields", []) or self.getColumnNames()
        for f in fields:
            if f not in showFields:
                continue
            data[f] = fields[f]

        if self.ExtraData:
            for f in self.ExtraData:
                if f == "dt":
                    data[f] = str(DateTime())
                else:
                    data[f] = getattr(request, f, "")
        data["waiting_list"] = self.waiting_list_is_open(
            max_attendees, waiting_list_size
        )
        self.addDataRow(data)

    def waiting_list_is_open(self, max_attendees, waiting_list_size):
        if not waiting_list_size:
            return False
        if not max_attendees:
            return False
        registrants, waiting_list = self.get_registrants()

        if registrants < max_attendees:
            return False

        return waiting_list_size > waiting_list

    def has_reached_limit(self, max_attendees, waiting_list_size):
        if not max_attendees:
            return False
        registrants, waiting_list = self.get_registrants()
        if registrants < max_attendees:
            return False
        if not waiting_list_size:
            return True
        return waiting_list >= waiting_list_size

    def has_reached_subscriptions_limit(self, max_attendees, waiting_list_size):
        if not max_attendees:
            return False
        registrants, waiting_list = self.get_registrants()
        return registrants >= max_attendees

    def get_registrants(self):
        registrants = 0
        waiting_list = 0
        for registrant in self._storage.values():
            if registrant.get("waiting_list", False):
                waiting_list += 1
            else:
                registrants += 1
        return registrants, waiting_list


RegistrantDataAction = ActionFactory(
    RegistrantData,
    _(u"label_registrant_data_action", default=u"Registrant Data"),
    "collective.easyform.AddDataSavers",
)

RegistrantDataHandler = BaseHandler(RegistrantData)
