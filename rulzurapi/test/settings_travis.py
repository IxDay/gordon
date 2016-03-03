"""Travis test setting conf

Redifined the database name, host, user and password to allows
direct connection to the travis postgres instance

"""
# pylint: disable=relative-import, no-member
import settings

settings.DATABASE['host'] = 'localhost'
settings.DATABASE['database'] = 'rulzurdb_test'
settings.DATABASE['user'] = 'postgres'
settings.DATABASE['password'] = ''
