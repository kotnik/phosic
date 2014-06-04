#!/usr/bin/env python2

from migrate.versioning import api
from app import config

v = api.db_version(
    config['SQLALCHEMY_DATABASE_URI'], config['SQLALCHEMY_MIGRATE_REPO']
)
api.downgrade(
    config['SQLALCHEMY_DATABASE_URI'],
    config['SQLALCHEMY_MIGRATE_REPO'],
    v - 1
)
print 'Current database version: ' + str(api.db_version(
    config['SQLALCHEMY_DATABASE_URI'], config['SQLALCHEMY_MIGRATE_REPO']
))
