# -*- coding:utf-8 -*-

from fabric.api import local


def compile_coffee():
    ''' Compiles all coffeescript files to javascript '''
    local('./scripts/coffee_compiler.js --all')


def compile_less():
    ''' Compiles less to css '''
    local('lessc static/css/style.less > static/css/style.css')


def freeze():
    ''' Creates static html files '''
    local('python site.py build')


def work():
    ''' Start watchers (coffee and less) '''
    # compilers
    local('./scripts/coffee_compiler.js &')
    local('./scripts/less_compiler.js &')


def build():
    compile_coffee()
    compile_less()
    freeze()


def run():
    local('python site.py')
