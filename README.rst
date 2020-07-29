.. This README is meant for consumption by humans and pypi. Pypi can render rst files so please do not use Sphinx features.
   If you want to learn more about writing documentation, please check out: http://docs.plone.org/about/documentation_styleguide.html
   This text does not appear on pypi or github. It is a comment.

========================================
Collective Easyform: Registration plugin
========================================

Plugin for collective.easyform that allows to manage a subscription form.

With this product installed, when you create a new **Easyform** content-type, there will be a new "Registration" tab in edit form.

You can set the max number of attendees, a waiting list and open and close dates.

Subscription logic
------------------

Users can subscribe to the form if:

- Current date is between open and close date
- There are still available slots
- Available slots are full but there is a waiting list

Contact registrants
-------------------

You can send messages to registrants (and waiting list) to keep them updated.


Translations
------------

This product has been translated into

- English
- Italian


Installation
------------

Install collective.easyformplugin.registration by adding it to your buildout::

    [buildout]

    ...

    eggs =
        collective.easyformplugin.registration


and then running ``bin/buildout``


Contribute
----------

.. image:: https://github.com/collective/collective.easyformplugin.registration/workflows/Build%20&%20Test/badge.svg?event=push
    :target:https://github.com/collective/collective.easyformplugin.registration/actions?query=workflow%3A%22Build+%26+Test%22

- Issue Tracker: https://github.com/collective/collective.easyformplugin.registration/issues
- Source Code: https://github.com/collective/collective.easyformplugin.registration


License
-------

The project is licensed under the GPLv2.
