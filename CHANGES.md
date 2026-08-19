# Changelog

## 3.0.0 (unreleased)

- Breaking: Plone 6.2 only; Python 3.10-3.14. [jensens]
- Breaking: Native namespace packages (PEP 420) - the `collective` and
  `collective.easyformplugin` namespace `__init__.py` files are gone. [jensens]
- Packaging: `pyproject.toml` with hatchling + hatch-vcs; the git tag is the
  single source of the version. `setup.py`, `setup.cfg`, `MANIFEST.in`,
  `buildout.cfg` and `requirements.txt` removed. [jensens]
- CI: GitHub Actions (qa/tests/ci/release) with uv; tests run against the
  Plone 6.2 constraints with zope.testrunner; releases are published to PyPI
  via trusted publishing. [jensens]
- Code style: ruff check and ruff format replace black/isort. As part of this
  the `type` argument of `RegistrationFormForm.set_status_message` was renamed
  to `message_type` (it shadowed the builtin). [jensens]
- `update_locale` uses `importlib.resources` instead of `pkg_resources` and no
  longer depends on a buildout tree. [jensens]
- Tests: use the Plone 6 installer API (`is_product_installed`,
  `uninstall_product`). [jensens]
- Fix adding of EasyForm field and action schemata from context with encoding information. [thet]
- Enhanced gender forms of German translation. [jensens]

## 2.0.0 (2022-05-31)

- Update IRegistrationForm Schema [1letter]
- Add Shortname for behavior [1letter]
- Update translation and add German language. [jensens]
- Development: Move from TravisCI to Github Actions. [jensens]
- Fix setup test. [jensens]
- Black and isort code formating. [jensens]
- Breaking: Drop support for Plone < 5.2. [jensens]
- Breaking: Drop Python 2 support, add Python 3 support. [jensens]

## 1.0.0 (2020-03-06)

- Initial release. [cekk]
