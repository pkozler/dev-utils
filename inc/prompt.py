from classes.db import Db
from classes.util import to_prefixed, to_camel_case


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


def enter_columns_to_update(db: Db, table_name: str, pk_column: str = '', update_column: str = ''):
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
