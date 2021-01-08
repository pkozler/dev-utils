import getopt

from sqlalchemy import Table, Column

import db.models

from db.models import Base as Entity
from classes.resource import Resource


def get_tab_col(arg: str) -> (str, str):
    names = str.split(arg, '.')

    if len(names) <= 1:
        return '', ''

    return names[0], names[1]


def enter_table_to_update(module, table_name: str = ''):
    if not table_name:
        table_name = input('Enter table name: ')
    else:
        table_name = str(table_name)



    class_name = to_camel_case(table_name)

    if not hasattr(module, class_name):
        print(f'{class_name} is not in {module}!')
        class_name = to_prefixed(table_name)

        if not hasattr(module, class_name):
            print(f'{class_name} is not in {module}!')
            exit(1)

    table_entity = getattr(module, class_name)

    return table_entity


def enter_columns_to_update(db: Resource, table_name: str, pk_column: str = '', update_column: str = ''):
    if not db.has_table(table_name):
        print(f'{table_name} is not in {db.dbname}!')
        exit(1)

    table_fields = db.get_table_detail(table_name).get('columns')
    column_names = [col['name'] for col in table_fields]

    if not len(column_names):
        print(f'{table_name} has not any columns!')
        exit(1)

    if not pk_column:
        pk_column = input('Enter primary key column: ')
    else:
        pk_column = str(pk_column)

    if pk_column not in column_names:
        print(f'{pk_column} is not in {table_name}!')
        exit(1)

    if not update_column:
        update_column = input('Enter column to update: ')
    else:
        update_column = str(update_column)

    if update_column not in column_names:
        print(f'{update_column} is not in {table_name}!')
        exit(1)

    return table_fields


def get_entity_field(a: str) -> (Entity or Table, Column):
    (tab, col) = get_tab_col(a)
    print(f'column: {tab}.{col}')

    is_class = hasattr(db.models, to_camel_case(tab))
    is_table = hasattr(db.models, to_prefixed(tab))

    if not (is_class or is_table):
        raise Exception(f"Error: invalid table {tab}")

    entity = getattr(db.models, to_camel_case(tab)) if is_class else getattr(db.models, to_prefixed(tab))
    is_field = hasattr(entity, col)

    if not is_field:
        raise Exception(f"Error: invalid column '{tab}.{col}'")

    field = getattr(entity, col)

    return entity, field


def get_pk_fk(args: []) -> (Entity or Table, Column, Entity or Table, Column):
    opts, args = getopt.getopt(args, [], ['fkcol=', 'pkcol='])

    valid_opts = {'--pkcol': (None, None), '--fkcol': (None, None)}
    valid_opts_keys = list(valid_opts.keys())

    for o, a in opts:
        if o not in valid_opts_keys:
            raise Exception(f"Error: invalid option '{o}'")

        for vk in valid_opts_keys:
            if o != vk:
                continue

            entity, field = get_entity_field(a)
            valid_opts[vk] = (entity, field)

            break

    return tuple([value for v in valid_opts.values() for value in v])
