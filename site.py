#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals  # unicode by default

import sys

from flask import Flask
from flask import render_template
from flask_flatpages import FlatPages
from flask_frozen import Freezer

# Create the Flask app
app = Flask(__name__)
# Load common settings
app.config.from_pyfile('settings/common.py')
# Add the FlatPages extension
pages = FlatPages(app)
# Add the Frozen extension
freezer = Freezer(app)


#
# Localization
#

locales = ['en', 'pt-br']
default_locale = 'pt-br'


#
# Utils
#

@freezer.register_generator
def default_locale_urls():
    ''' Genarates the urls for default locale without prefix. '''
    for page in pages:
        yield '/{}/'.format(remove_l10n_prefix(page.path))


@freezer.register_generator
def page_urls():
    ''' Genarates the urls with locale prefix. '''
    for page in pages:
        yield '/{}/'.format(page.path)


def has_l10n_prefix(path):
    ''' Verifies if the path have a localization prefix. '''
    return reduce(lambda x, y: x or y, [path.startswith(l) for l in locales])


def add_l10n_prefix(path, locale=default_locale):
    '''' Add localization prefix if necessary. '''
    return path if has_l10n_prefix(path) else '{}/{}'.format(locale, path)


def remove_l10n_prefix(path, locale=default_locale):
    ''' Remove specific localization prefix. '''
    return path if not path.startswith(locale) else path[(len(locale) + 1):]

# Add remove_l10n_prfix accessible to Jinja
app.jinja_env.globals.update(remove_l10n_prefix=remove_l10n_prefix)


#
# Routes
#

@app.route('/')
def root():
    ''' Main page '''
    return render_template('root.html', pages=pages, page=None)


@app.route('/<path:path>/')
def page(path):
    ''' All pages from markdown files '''
    page = pages.get_or_404(add_l10n_prefix(path))
    template = page.meta.get('template', 'page.html')
    return render_template(template, page=page)


#
# Main
#

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == "build":
        freezer.freeze()
    else:
        app.run(port=8000)
