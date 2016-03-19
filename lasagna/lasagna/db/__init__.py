"""Database module, contains all the database related codebase
"""
import playhouse.pool

database = playhouse.pool.PooledPostgresqlExtDatabase(
    None, register_hstore=False
)

schema = 'gordon'
