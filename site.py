#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals  # unicode by default

import sys
from collections import OrderedDict

import markdown

from flask import Flask
from flask import render_template, redirect, url_for
from flaskext.babel import Babel
from flask_flatpages import FlatPages
from flask_frozen import Freezer


# TODO:
# * Get babel locale from request path


# Create the Flask app
app = Flask(__name__)

# Load settings
app.config.from_pyfile('settings/common.py')
app.config.from_pyfile('settings/local_settings.py', silent=True)

# Add the babel extension
babel = Babel(app)

# Add the FlatPages extension
pages = FlatPages(app)

# Add the Frozen extension
freezer = Freezer(app)


#
# Utils
#

# Frozen url generators

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


# l10n helpers

def has_l10n_prefix(path):
    ''' Verifies if the path have a localization prefix. '''
    return reduce(lambda x, y: x or y, [path.startswith(l)
                  for l in app.config.get('AVAILABLE_LOCALES', [])])


def add_l10n_prefix(path, locale=app.config.get('DEFAULT_LOCALE')):
    '''' Add localization prefix if necessary. '''
    return path if has_l10n_prefix(path) else '{}/{}'.format(locale, path)


def remove_l10n_prefix(path, locale=app.config.get('DEFAULT_LOCALE')):
    ''' Remove specific localization prefix. '''
    return path if not path.startswith(locale) else path[(len(locale) + 1):]

# Make remove_l10n_prefix accessible to Jinja
app.jinja_env.globals.update(remove_l10n_prefix=remove_l10n_prefix)


# Structure helpers

def render_markdown(text):
    ''' Render Markdown text to HTML. '''
    extensions = ['attr_list', 'headerid(forceid=False)']
    return markdown.markdown(text, extensions)

app.config['FLATPAGES_HTML_RENDERER'] = render_markdown


def create_pages_tree(pages):
    ''' Create a tree to be used to render navigation menu and site map. '''

    def _attach(branch, trunk, page):
        ''' attach branches to trunk. '''
        parts = branch.split('/', 1)
        if len(parts) == 1:  # is a page
            if parts[0] in trunk:
                trunk[parts[0]]['index'] = page
            else:
                trunk[parts[0]] = {'index': page}
        else:
            node, others = parts
            if node not in trunk:
                trunk[node] = {}  # create new branch
            _attach(others, trunk[node], page)

    def _sorted_tree(trunk):
        ''' sort the tree '''
        if not trunk or not isinstance(trunk, dict):
            return trunk

        def _sort(item):
            if not isinstance(item[1], dict):
                return item
            page = item[1].get('index')
            pos = page.meta.get('pos', 1000) if page else 1000
            return '{:04}{}'.format(pos, item[0])

        for key, branch in trunk.items():
            if isinstance(branch, dict):
              trunk[key] = _sorted_tree(branch)
        return OrderedDict(sorted(trunk.items(), key=_sort))

    tree = {}
    for page in pages:
        _attach(page.path, tree, page)
    return _sorted_tree(tree)

tree = create_pages_tree(pages)


#
# Routes
#

@app.route('/')
def root():
    ''' Main page '''
    return render_template('root.html', page=None, pages=pages, tree=tree)


@app.route('/<path:path>/')
def page(path):
    ''' All pages from markdown files '''

    # Get the page
    page = pages.get_or_404(add_l10n_prefix(path))

    # Get custom template
    template = page.meta.get('template', 'page.html')

    # Verify if need redirect
    redirect_ = page.meta.get('redirect', None)
    if redirect_:
        return redirect(url_for('page', path=redirect_))

    # Render the page
    return render_template(template, page=page, pages=pages, tree=tree)


#
# Main
#

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'build':
        freezer.freeze()
    else:
        app.run(port=8000)
