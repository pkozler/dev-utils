"""
    Použití: provede rychlý průzkum tabulek v zadané databázi, pro každé schéma
    vypíše obsažené tabulky, pro každou z těchto tabulek vypíše seznam jejích sloupců
    a dále vypíše seznam všech cizích klíčů seřazený podle vynuceného pořadí vytáření tabulek.
"""


from classes.resource import Resource


def list_table_structure(db: Resource):
    total_table_count = 0
    total_columns_sum = 0

    for table_name in db.get_inspector().get_table_names(schema=db.dbname):
        schema_table = '.'.join([db.dbname, table_name])
        total_table_count += 1

        columns_list = []
        for column in db.get_inspector().get_columns(table_name, schema=db.dbname):
            columns_list.append(str(column['name']))

        column_count = len(columns_list)
        total_columns_sum += column_count
        column_names = ', '.join(columns_list)

        print("{}. Table: {}\n\t- {} cols: {}\n---\n".format(
            total_table_count, schema_table, column_count, column_names))

    print("=== A total of {} columns in {} tables found in {} schema. ===\n".format(
        total_columns_sum, total_table_count, db.dbname))


def list_sorted_table_and_fkc_names(db: Resource):
    print("Sorted table and foreign key constraint names:\n---\n")

    sorted_table_and_fkc_names = db.get_inspector().get_sorted_table_and_fkc_names(db.dbname)

    for s in sorted_table_and_fkc_names:
        print(f"{s}")

    print()


def list_schemas(db: Resource):
    schemas = db.get_inspector().get_schema_names()

    print("Scanning table structure of DB: %s\n---\n".format(" + ".join(schemas)))

    for schema in schemas:
        # skipping information_schema:
        # if schema != db.dbname:
        #     continue

        list_table_structure(db)
        input("Enter to proceed with schema:" + schema)

        list_sorted_table_and_fkc_names(db)
        input("Enter to finish this schema:" + schema)

    print("All tables finished!\n")


resource = Resource.connect()
list_schemas(resource)
