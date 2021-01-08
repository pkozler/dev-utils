from sqlalchemy import Table

import utils.db.models
from db.models import Base as Entity
from classes.resource import Resource


class Model:

    def __init__(self, db: Resource, table_name: str):
        self._db = db

        if not db.has_table(table_name):
            raise IndexError(f'{table_name} is not in {self._db.dbname}!')

        self.__table_name = table_name

        module = utils.db.models
        class_name = Model.to_camel_case(table_name)
        is_class_entity = True

        if not hasattr(module, class_name):
            class_name = Model.to_prefixed(table_name)
            is_class_entity = False

            if not hasattr(module, class_name):
                raise IndexError(f'{class_name} is not in {module}!')

        self.__is_class_entity = is_class_entity
        self.__class_name = class_name
        self.__entity = getattr(module, class_name)

        self._columns, self._pk_constraint, self._foreign_keys = None, None, None,
        self._indexes, self._unique_constraints, self._check_constraints = None, None, None,

    @property
    def is_class_entity(self) -> bool:
        return self.__is_class_entity

    @property
    def table_name(self) -> str:
        return self.__table_name

    @property
    def class_name(self) -> str:
        return self.__class_name

    @property
    def entity(self) -> Entity or Table:
        return self.__entity

    def get_columns(self):
        if self._columns is None:
            self._columns = self._db.get_inspector().get_columns(self.table_name, schema=self._db.dbname)

        return self._columns

    def get_pk_constraint(self):
        if self._pk_constraint is None:
            self._pk_constraint = self._db.get_inspector().get_pk_constraint(self.table_name, schema=self._db.dbname)

        return self._pk_constraint

    def get_foreign_keys(self):
        if self._foreign_keys is None:
            self._foreign_keys = self._db.get_inspector().get_foreign_keys(self.table_name, schema=self._db.dbname)

        return self._foreign_keys

    def get_indexes(self):
        if self._indexes is None:
            self._indexes = self._db.get_inspector().get_indexes(self.table_name, schema=self._db.dbname)

        return self._indexes

    def get_unique_constraints(self):
        if self._unique_constraints is None:
            self._unique_constraints = self._db.get_inspector().get_unique_constraints(self.table_name, schema=self._db.dbname)

        return self._unique_constraints

    def get_check_constraints(self):
        if self._check_constraints is None:
            self._check_constraints = self._db.get_inspector().get_check_constraints(self.table_name, schema=self._db.dbname)

        return self._check_constraints

    @classmethod
    def to_prefixed(cls, snake_str: str) -> str:
        return f"t_{snake_str}"

    @classmethod
    def to_camel_case(cls, snake_str: str) -> str:
        components = snake_str.split('_')

        return components[0].title() + ''.join(x.title() for x in components[1:])
