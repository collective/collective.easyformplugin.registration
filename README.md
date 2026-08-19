# Collective Easyform: Registration plugin

Plugin for collective.easyform that allows to manage a subscription form.

With this product installed, when you create a new **Easyform** content-type,
there will be a new "Registration" tab in edit form.

You can set the max number of attendees, a waiting list and open and close
dates.

## Subscription logic

Users can subscribe to the form if:

- Current date is between open and close date
- There are still available slots
- Available slots are full but there is a waiting list

## Contact registrants

You can send messages to registrants (and waiting list) to keep them updated.

## Translations

This product has been translated into

- English
- Italian
- German

## Installation

Add `collective.easyformplugin.registration` to the dependencies of your Plone
project, for example in `pyproject.toml`:

```toml
dependencies = [
    "Products.CMFPlone",
    "collective.easyformplugin.registration",
]
```

Then install the add-on in the Plone site control panel.

Requires Plone 6.2 and Python 3.10 or newer.

## Contribute

[![CI](https://github.com/collective/collective.easyformplugin.registration/actions/workflows/ci.yaml/badge.svg)](https://github.com/collective/collective.easyformplugin.registration/actions/workflows/ci.yaml)

- Issue Tracker: https://github.com/collective/collective.easyformplugin.registration/issues
- Source Code: https://github.com/collective/collective.easyformplugin.registration

See [DEVELOP.md](DEVELOP.md) for the development setup and
[RELEASE.md](RELEASE.md) for the release process.

## License

The project is licensed under the GPLv2.
