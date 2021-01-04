"""
    Použití: v tabulce např. sales_flat_order nastaví hodnoty created_at náhodně
    z intervalu '2012-01-01' až '2020-12-31', aby pro záznamy X a Y platilo,
    že pokud  X.entity_id  < Y.entity_id , pak i X.created_at < Y.created_at"
    (typický problém při testování BI metrik, kde chceme mít zdrojová data
    ideálně z několika let nazpátek, ale pro úsporu místa máme na devu data
    jen za několik posledních měsíců).
"""

from datetime import datetime
from math import sqrt, ceil

from sqlalchemy import func

import db.models
from classes.generator import Generator
from classes.db import Db

# init:
from classes.types import DATE_TYPES
from inc.prompt import enter_table_to_update, enter_columns_to_update

table_name = 'sales_flat_order'
id_column_name = 'entity_id'
dt_column_name = 'created_at'

# module = importlib.import_module('db.models')
resource = Db.connect()

entity = enter_table_to_update(db.models, table_name=table_name)

print(f"{entity}:\n")

fields = enter_columns_to_update(resource, table_name, pk_column=id_column_name, update_column=dt_column_name)

for col in fields:
    col_type = str.lower(str(col['type']))

    for dt in DATE_TYPES:
        if col_type.startswith(dt):
            print(f"{col['name']} -> {col['type']}")

print(f"({len(fields)})\n")

id_col = getattr(entity, id_column_name)
dt_col = getattr(entity, dt_column_name)

# main:

session = resource.get_session()

min_max_date = session.query(
    func.min(dt_col),
    func.max(dt_col),
    func.count(id_col), )

(min_date, max_date, date_count) = min_max_date.first()

print(min_max_date)
print(f"{dt_column_name}: {min_date} - {max_date} ({date_count})")
print(f"{id_column_name} -> {Generator.DEFAULT_MIN_DATE} .. {dt_column_name} .. {Generator.DEFAULT_MAX_DATE}")

datetime_list = Generator.generate_datetime_list(Generator.DEFAULT_MIN_DATE, Generator.DEFAULT_MAX_DATE, date_count)
id_list = session.query(id_col).order_by(id_column_name).all()

# print(id_list)
total_size = len(id_list)

if total_size != len(datetime_list):
    print(f'Error: id_list_size <> dt_list_size!')
    exit(1)

batch_size = int(round(sqrt(float(total_size))))
print(f"Total items: {total_size} ({batch_size} per batch)\n")

input("Enter to proceed: ")
last_cnt = 0

for cnt, val in enumerate(id_list):
    # print(f"{cnt}: {id_col} = {val[0]}; {dt_col} = {datetime_list[cnt]}")

    try:
        res = session.query(entity).filter(id_col == id_list[cnt][0]).update(
            {dt_column_name: datetime_list[cnt]})

        # print(f"{cnt}: {val[0]} ... {res} ")

        if (cnt + 1) % batch_size:
            continue

        session.commit()
        print(f"Saved #{last_cnt} -> #{cnt}")
        last_cnt = cnt

    except IndexError as e:
        print(f"Error: *** {e} ***")

session.commit()
print(f"Saved #{last_cnt} -> #{total_size}")

print(f"Completed! ({int(ceil(float(total_size) / float(batch_size)))} batches)")
