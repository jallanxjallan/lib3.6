#!/home/jeremy/PythonEnv/bin/python
# -*- coding: utf-8 -*-
#
#  module.py
#  
#  Copyright 2019 Jeremy Allan <jeremy@jeremyallan.com>

import sys
import os

sys.path.append('/home/jeremy/Library/')

from data_storage.cherrytree import CherryTree


def connect_db():
    """Connects to the specific database."""
    rv = CherryTree(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv


def init_db():
    """Initializes the database."""
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()


@app.cli.command('initdb')
def initdb_command():
    """Creates the database tables."""
    init_db()
    print('Initialized the database.')


def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db


@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()
