#!/usr/bin/python
# -*- coding: utf-8 -*-
 
import os, sys
import locale
import gettext

#  The translation files will be under
#  @LOCALE_DIR@/@LANGUAGE@/LC_MESSAGES/@APP_NAME@.mo
APP_NAME = "game"

# App dir
APP_DIR = os.path.dirname(os.path.realpath(__file__))
LOCALE_DIR = os.path.join(APP_DIR, 'i18n') # .mo files will then be located in APP_Dir/i18n/LANGUAGECODE/LC_MESSAGES/

# Provide a list, and gettext
DEFAULT_LANGUAGES = os.environ.get('LANG', '').split('.')
DEFAULT_LANGUAGES += ['cs_US']

lc, encoding = locale.getdefaultlocale()
if lc:
    languages = [lc]

# Concat all languages (env + default locale),
#  and here we have the languages and location of the translations
languages += DEFAULT_LANGUAGES
mo_location = LOCALE_DIR

# Lets tell those details to gettext
#  (nothing to change here for you)
gettext.install(True, localedir=None, unicode=1)

gettext.find(APP_NAME, mo_location)

gettext.textdomain (APP_NAME)

gettext.bind_textdomain_codeset(APP_NAME, 'UTF-8')


language = gettext.translation(APP_NAME, mo_location, languages=languages, fallback=True)