from classes.model import Model
from classes.prompt import Prompt
from classes.resource import Resource
from classes.format import Format

TABLE = 'table'


def print_table(entity: Model) -> None:
    Format.print("\n")
    Format.print(f"Table_name: '{entity.table_name}'\n", underline=True)

    Format.print('Columns:\n')
    for column in entity.get_all_columns():
        col_str = f"{column['name']}: [{str.lower(str(column['type']))}{'?' if ('nullable' in column) else ''}] {'' if column['default'] is None else ('| ' + str(column['default']) + '')}{'[...]' if ('autoincrement' in column and column['autoincrement']) else ''}"
        Format.print(f"{col_str}", bold=True)
    Format.print()

    Format.print('Pk_constraint:\n')
    pk_str = '-'.join(entity.get_pk_constraint()['constrained_columns'])
    Format.print_primary(f"{pk_str}", bold=True)
    Format.print()

    Format.print('Foreign_keys:\n')
    for foreign_key in entity.get_all_foreign_keys():
        fk_str = f"{', '.join(foreign_key['constrained_columns'])}: {foreign_key['referred_table']}({', '.join(foreign_key['referred_columns'])})"
        Format.print_success(f"{fk_str}", bold=True)
    Format.print()

    Format.print('Indexes:\n')
    for index in entity.get_all_indexes():
        idx_str = f"{index['name']}: ({', '.join(index['column_names'])}){'[!]' if {index['unique']} else ''}"
        Format.print_info(f"{idx_str}", bold=True)
    Format.print()

    Format.print('Unique_constraints:\n')
    for unique_constraint in entity.get_all_unique_constraints():
        uq_str = f"{unique_constraint['name']}: ({', '.join(unique_constraint['column_names'])})"
        Format.print_warning(f"{uq_str}", bold=True)
    Format.print()

    Format.print('Check_constraints:\n')
    for check_constraint in entity.get_all_check_constraints():
        chk_str = f"{check_constraint['name']}: {check_constraint['sqltext']})"
        Format.print_danger(f"{chk_str}", bold=True)
    Format.print()


args = '--table sales_flat_order'.split()

db = Resource.connect()

cmd = Prompt([TABLE])
table = cmd.set_args(args).get_item(TABLE)
entity = Model(db, table)

print_table(entity)
