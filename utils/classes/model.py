from sqlalchemy import Table, Column
from typing import Tuple, Set

import db.models
from db.models import Base as Entity
from classes.resource import Resource


class Model:

    def __init__(self, resource: Resource, table_name: str):
        self._db = resource

        if not resource.has_table(table_name):
            raise IndexError(f'{table_name} is not in {self._db.dbname}!')

        self.__table_name = table_name

        class_name = Model.to_camel_case(table_name)
        is_class_entity = True

        module = db.models

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

    def get_all_columns(self) -> []:
        if self._columns is None:
            self._columns = self._db.get_inspector().get_columns(self.table_name, schema=self._db.dbname)

        return self._columns or []

    def get_pk_constraint(self) -> {}:
        if self._pk_constraint is None:
            self._pk_constraint = self._db.get_inspector().get_pk_constraint(self.table_name, schema=self._db.dbname)

        return self._pk_constraint or {}

    def get_all_foreign_keys(self) -> []:
        if self._foreign_keys is None:
            self._foreign_keys = self._db.get_inspector().get_foreign_keys(self.table_name, schema=self._db.dbname)

        return self._foreign_keys or []

    def get_all_indexes(self) -> []:
        if self._indexes is None:
            self._indexes = self._db.get_inspector().get_indexes(self.table_name, schema=self._db.dbname)

        return self._indexes or []

    def get_all_unique_constraints(self) -> []:
        if self._unique_constraints is None:
            self._unique_constraints = self._db.get_inspector().get_unique_constraints(self.table_name, schema=self._db.dbname)

        return self._unique_constraints or []

    def get_all_check_constraints(self) -> []:
        if self._check_constraints is None:
            self._check_constraints = self._db.get_inspector().get_check_constraints(self.table_name, schema=self._db.dbname)

        return self._check_constraints or []

    def get_column(self, name: str) -> Column or None:
        for x in self.get_all_columns():
            if (x['name'] == name) and hasattr(self.entity, name):
                return getattr(self.entity, name)

        return None

    def get_primary_key(self) -> (Column, ...):
        pk_columns = [self.get_column(c) for c in self.get_pk_constraint()['constrained_columns']]

        return tuple(pk_columns)

    def get_foreign_key(self, names: [str]) -> (Column, ...) or ():
        fk_columns = []

        for cl in self.get_all_foreign_keys():

            if set(names) == set(cl['constrained_columns']):
                fk_columns = [self.get_column(c) for c in cl['constrained_columns']]

                return tuple(fk_columns)

        return tuple(fk_columns)

    def get_index(self, name: str) -> {} or None:
        for x in self.get_all_indexes():
            if x['name'] == name:
                return x

        return None

    def get_unique_constraint(self, name: str) -> {} or None:
        for x in self.get_all_unique_constraints():
            if x['name'] == name:
                return x

        return None

    def get_check_constraint(self, name: str) -> {} or None:
        for x in self.get_all_check_constraints():
            if x['name'] == name:
                return x

        return None

    @classmethod
    def to_prefixed(cls, snake_str: str) -> str:
        return f"t_{snake_str}"

    @classmethod
    def to_camel_case(cls, snake_str: str) -> str:
        components = snake_str.split('_')

        return components[0].title() + ''.join(x.title() for x in components[1:])
