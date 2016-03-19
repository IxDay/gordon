"""Travis test setting conf

Redifined the database name, host, user and password to allows
direct connection to the travis postgres instance

"""
import lasagna.settings as settings

settings.DATABASE['host'] = 'localhost'
settings.DATABASE['database'] = 'potato_test'
settings.DATABASE['user'] = 'postgres'
settings.DATABASE['password'] = ''
