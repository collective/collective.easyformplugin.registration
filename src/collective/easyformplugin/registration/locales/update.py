from importlib.resources import files
from pathlib import Path

import os
import subprocess


domain = "collective.easyformplugin.registration"

# Package directory (…/src/collective/easyformplugin/registration) and the
# locales folder inside it. i18ndude is expected on the PATH (e.g. installed
# into the virtualenv), the former buildout ./bin/i18ndude is gone.
package_path = Path(str(files(domain)))
locale_path = package_path / "locales"
i18ndude = "i18ndude"


def locale_folder_setup():
    cwd = os.getcwd()
    os.chdir(locale_path)
    try:
        languages = [d for d in os.listdir(".") if os.path.isdir(d)]
        for lang in languages:
            if "LC_MESSAGES" in os.listdir(lang):
                continue
            os.mkdir(f"{lang}/LC_MESSAGES/")
            cmd = f"msginit --locale={lang} --input={domain}.pot --output={lang}/LC_MESSAGES/{domain}.po"
            subprocess.call(cmd, shell=True)
    finally:
        os.chdir(cwd)


def _rebuild():
    cmd = f"{i18ndude} rebuild-pot --pot {locale_path}/{domain}.pot --create {domain} {package_path}"
    subprocess.call(cmd, shell=True)


def _sync():
    cmd = f"{i18ndude} sync --pot {locale_path}/{domain}.pot {locale_path}/*/LC_MESSAGES/{domain}.po"
    subprocess.call(cmd, shell=True)


def update_locale():
    locale_folder_setup()
    _sync()
    _rebuild()
