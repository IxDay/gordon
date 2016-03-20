"""Base test setting conf

Redifined the database name, host and password

Ensure that logs are not polluted with debug output
(if debugging the test this option needs to be reactivated)

Force application state to debug
"""
import lasagna.settings as settings

TESTING = True
DEBUG = False


settings.DATABASE['host'] = 'potato'
settings.DATABASE['database'] = 'potato_test'
settings.DATABASE['password'] = 'password'
