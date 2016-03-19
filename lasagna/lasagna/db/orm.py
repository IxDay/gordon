"""Peewee ORM hacking"""
import re

import peewee
import playhouse

import lasagna.utils.helpers as helpers

class EnumField(peewee.Field):
    """Enum field

    define an enum field in your model like this:
    EnumField(choices=['a', 'b', 'c'])
    """
    db_field = 'enum'

    def pre_field_create(self, _):
        """Create the enum type"""
        field = 'e_%s' % self.name

        self.get_database().get_conn().cursor().execute(
            'DROP TYPE IF EXISTS %s;' % field
        )

        query = self.get_database().get_conn().cursor()
        tail = ', '.join(["'%s'"] * len(self.choices)) % tuple(self.choices)
        q = 'CREATE TYPE %s AS ENUM (%s);' % (field, tail)
        query.execute(q)

    def post_field_create(self, _):
        """Once creation succeed register the enum name as field name"""
        self.db_field = 'e_%s' % self.name

    def __ddl_column__(self, _):
        return peewee.SQL('e_%s' % self.name)

    def db_value(self, value):
        if value not in self.choices:
            raise ValueError('Invalid Enum Value "%s"' % value)
        return str(value)


class DirectionField(peewee.Field):
    """Custom database direction field (postgres custom type)"""
    db_field = 'direction'

    def db_value(self, value):
        return '("%s", "%s")' % (value[0], value[1])

    def python_value(self, value):
        title, text = value.strip('()').split(',')

        title = title.strip('"')
        text = text.strip('"')[1:]
        return helpers.Direction(title, text)


class ArrayField(playhouse.postgres_ext.ArrayField):
    """Improved peewee ArrayField

    As peewee does not handle correctly the indexing of array, this extending
    fix this behaviour.
    Additionnaly, it supports complex type insertion without explicit casting
    (only first level, nested aren't supported).
    """
    parser = re.compile(r'\(.*?\)')
    default_index_type = None

    def db_value(self, value):
        def stringify(elt):
            """Stringifies an array element

            If the element is a complex object it is returned as a jointure
            of its attrs
            If the element is a string, simply return as is
            """
            if helpers.is_iterable(elt):
                return '"(%s)"' % ', '.join(elt)
            else:
                return str(elt)

        return '{%s}' % ', '.join(
            stringify(elt) for elt in super(ArrayField, self).db_value(value)
        )

    def python_value(self, value):
        if isinstance(value, str):
            values = [value.replace('\\"', '"')
                      for value in self.parser.findall(value)]
        else:
            values = value

        return [self.__field.python_value(value) for value in values]
