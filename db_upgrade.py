#!/usr/bin/env python2

from migrate.versioning import api
from app import config

api.upgrade(config['SQLALCHEMY_DATABASE_URI'], config['SQLALCHEMY_MIGRATE_REPO'])
print 'Current database version: ' + str(api.db_version(
    config['SQLALCHEMY_DATABASE_URI'], config['SQLALCHEMY_MIGRATE_REPO']
))
