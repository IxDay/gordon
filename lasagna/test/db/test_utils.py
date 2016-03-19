import time
import threading

import peewee

import lasagna.db as db
import lasagna.db.utils as db_utils


def test_lock_table(gen_table):

    class TestTable(peewee.Model):
        id = peewee.PrimaryKeyField()
        name = peewee.CharField()

    def update(elt, new_name, wait=False):

        def get_rows():
            return test_table.select(test_table.name).dicts().execute()

        def update_query(id, name):
            return (test_table
                    .update(name=name)
                    .where(test_table.id == id)
                    .execute())

        with db.database.atomic():
            time.sleep(0.001) if wait else None
            update_query(elt.id, new_name)
            results.append(list(get_rows()).pop())

    results = []
    test_table = gen_table(TestTable)
    elt = test_table.create(name='foo')
    # first test without lock
    c_1 = threading.Thread(target=update, args=(elt, 'foo_updated_1', True))
    c_2 = threading.Thread(target=update, args=(elt, 'foo_updated_2', False))

    c_1.start()
    c_2.start()

    c_1.join()
    c_2.join()

    assert results == [{'name': 'foo_updated_2'}, {'name': 'foo_updated_1'}]
    del results[:]

    # second test with lock, order is inversed, as the first function takes
    # the lock first
    c_1 = threading.Thread(target=db_utils.lock(test_table)(update),
                           args=(elt, 'foo_updated_1', True))
    c_2 = threading.Thread(target=update, args=(elt, 'foo_updated_2', False))

    c_1.start()
    c_2.start()

    c_1.join()
    c_2.join()
    assert results == [{'name': 'foo_updated_1'}, {'name': 'foo_updated_2'}]
