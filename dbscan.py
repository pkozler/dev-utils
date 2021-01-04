
from classes.db import Db

db = Db.connect()
inspector = db.get_inspector()


def list_structure():
    schemas = inspector.get_schema_names()

    print("Scanning table structure of DB: %s\n---\n".format(" + ".join(schemas)))

    for schema in schemas:
        total_table_count = 0
        total_columns_sum = 0

        for table_name in inspector.get_table_names(schema=db.dbname):
            schema_table = '.'.join([schema, table_name])
            total_table_count += 1

            columns_list = []
            for column in inspector.get_columns(table_name, schema=db.dbname):
                columns_list.append(str(column['name']))
            column_count = len(columns_list)
            total_columns_sum += column_count
            column_names = ', '.join(columns_list)

            print("{}. Table: {}\n\t- {} cols: {}\n---\n".format(
                total_table_count, schema_table, column_count, column_names))

        print("=== A total of {} columns in {} tables found in {} schema. ===\n".format(
            total_columns_sum, total_table_count, schema))

    print("All tables finished!\n")


list_structure()

stfn = db.get_inspector().get_sorted_table_and_fkc_names(db.dbname)

for s in stfn:
    print(f"{s}")

print()
