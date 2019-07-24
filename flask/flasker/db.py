# -*- coding: utf-8 -*-

"""
    @author: xiaoshihu
    @file: db.py.py
    @time: 2019/7/24 9:57
    @desc: database connect
"""

import sqlite3

import click
# global var
from flask import current_app, g
from flask.cli import with_appcontext


# get db connect obj
def get_db():
    # check a var whether in a obj,like js.
    if 'db' not in g:
        # it just like obj in js,can add attr in a object everywhere
        g.db = sqlite3.connect(
            # file path,get config con
            current_app.config['DATABASE'],
            # not know
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        # config db connect
        g.db.row_factory = sqlite3.Row
    return g.db


# close db connect
# every request
def close_db(e=None):
    # like dict get method
    db = g.pop('db', None)
    if db is not None:
        db.close()
        print('close db connect!')


def init_db():
    # TODO: 2019/7/24 all request share a connect obj?
    db = get_db()
    # can we just use open？because we don't know the path of file,so
    # we config the path though app config,so when we want get this file
    # we should though current app?
    with current_app.open_resource('schema.sql') as f:
        # create table and clear data
        db.executescript(f.read().decode('utf8'))


# register command in flask shell
# and i doubt when the function be called?i point the doc
@click.command('init-db')
@with_appcontext
def init_db_command():
    init_db()
    # the information show when done
    click.echo('Initialized the database.')

def init_app(app):
    # register close connect function to app and be called when a request complete
    # TODO: 2019/7/24 close the connect when app teardown?not each request?
    app.teardown_appcontext(close_db)
    # register a command to flask shell
    app.cli.add_command(init_db_command)
