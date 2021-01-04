from inc.prompt import enter_table_to_update
from classes.db import Db
from classes.format import Format


def print_table(table_name, columns, pk_constraint, foreign_keys, indexes, unique_constraints, check_constraints) -> None:
    Format.print("\n")
    Format.print(f"Table_name: '{table_name}'\n", underline=True)

    Format.print('Columns:\n')
    for column in columns:
        col_str = f"{column['name']}: [{str.lower(str(column['type']))}{'?' if ('nullable' in column) else ''}] {'' if column['default'] is None else ('| ' + str(column['default']) + '')}{'[...]' if ('autoincrement' in column and column['autoincrement']) else ''}"
        Format.print(f"{col_str}", bold=True)
    Format.print()

    Format.print('Pk_constraint:\n')
    pk_str = '-'.join(pk_constraint['constrained_columns'])
    Format.print_primary(f"{pk_str}", bold=True)
    Format.print()

    Format.print('Foreign_keys:\n')
    for foreign_key in foreign_keys:
        fk_str = f"{', '.join(foreign_key['constrained_columns'])}: {foreign_key['referred_table']}({', '.join(foreign_key['referred_columns'])})"
        Format.print_success(f"{fk_str}", bold=True)
    Format.print()

    Format.print('Indexes:\n')
    for index in indexes:
        idx_str = f"{index['name']}: ({', '.join(index['column_names'])}){'[!]' if {index['unique']} else ''}"
        Format.print_info(f"{idx_str}", bold=True)
    Format.print()

    Format.print('Unique_constraints:\n')
    for unique_constraint in unique_constraints:
        uq_str = f"{unique_constraint['name']}: ({', '.join(unique_constraint['column_names'])})"
        Format.print_warning(f"{uq_str}", bold=True)
    Format.print()

    Format.print('Check_constraints:\n')
    for check_constraint in check_constraints:
        chk_str = f"{check_constraint['name']}: {check_constraint['sqltext']})"
        Format.print_danger(f"{chk_str}", bold=True)
    Format.print()


db = Db.connect()
(table) = enter_table_to_update(db)

print_table(*table)
