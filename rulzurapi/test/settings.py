"""Base test setting conf

Redifined the database name, host and password

Ensure that logs are not polluted with debug output
(if debugging the test this option needs to be reactivated)

Force application state to debug
"""
# pylint: disable=import-self, no-member
import settings

TESTING = True
DEBUG = False


settings.DATABASE['host'] = 'db'
settings.DATABASE['database'] = 'rulzurdb_test'
settings.DATABASE['password'] = 'password'
