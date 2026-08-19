# Developing

## Setup

Requires [uv](https://docs.astral.sh/uv/).

```bash
uv venv .venv --python 3.12
uv pip install -c https://dist.plone.org/release/6.2-latest/constraints.txt -e ".[test]" zope.testrunner
```

## Running tests

```bash
.venv/bin/zope-testrunner --all --test-path src
```

Run a single test module or method:

```bash
.venv/bin/zope-testrunner --test-path src -t test_setup
```

## Code quality

```bash
uvx ruff check --fix .
uvx ruff format .
```

CI runs `ruff check` and `ruff format --check`, so run both before pushing.

## Running a Plone site with the add-on

Use any Plone 6.2 instance (for example a
[cookiecutter-zope-instance](https://github.com/plone/cookiecutter-zope-instance)
setup) and install this package into its environment:

```bash
uv pip install -c https://dist.plone.org/release/6.2-latest/constraints.txt -e .
```

Then install the add-on in the Plone site control panel.

## i18n

Updating the translation catalog requires `i18ndude` and gettext
(`msginit`/`msgmerge`) on the PATH:

```bash
uv pip install i18ndude
.venv/bin/update_locale
```

## Releasing

See [RELEASE.md](RELEASE.md).
