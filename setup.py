# -*- coding: utf-8 -*-
"""Installer for the collective.easyformplugin.registration package."""

from setuptools import find_packages, setup

long_description = "\n\n".join(
    [
        open("README.rst").read(),
        open("CONTRIBUTORS.rst").read(),
        open("CHANGES.rst").read(),
    ]
)


setup(
    name="collective.easyformplugin.registration",
    version="1.0.1.dev0",
    description="Add a behavior to collective.easyform to manage registration forms",
    long_description=long_description,
    # Get more from https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Framework :: Plone :: 5.2",
        "Framework :: Plone :: 6.0",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
    ],
    keywords="Python Plone",
    author="Andrea Cecchi",
    author_email="andrea.cecchi85@gmail.com",
    url="https://github.com/collective/collective.easyformplugin.registration",
    license="GPL version 2",
    packages=find_packages("src", exclude=["ez_setup"]),
    namespace_packages=["collective", "collective.easyformplugin"],
    package_dir={"": "src"},
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "setuptools",
        "z3c.jbot",
        "collective.easyform[recaptcha]",
        "lxml",
    ],
    extras_require={"test": ["plone.app.testing", "plone.app.robotframework[debug]",]},
    entry_points="""
    [z3c.autoinclude.plugin]
    target = plone
    [console_scripts]
    update_locale = collective.easyformplugin.registration.locales.update:update_locale
    """,
)
