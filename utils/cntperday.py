"""
    Spočítá min, max, avg, atd. počtu záznamů v tabulce za 1 den, měsíc, rok.
"""

from sqlalchemy import func

from classes.model import Model
from classes.generator import Generator
from classes.resource import Resource
from classes.cmd import Cmd

TABLE, ID_COL, DATE_TIME_COL = 'table', 'idcol', 'dtcol'
# args = '--table sales_flat_order --idcol entity_id --dtcol created_at'.split()

resource = Resource.connect()
cmd = Cmd([TABLE, ID_COL, DATE_TIME_COL])

table = cmd.set_args().get_item(TABLE)
model = Model(resource, table)
entity = model.entity

print(f"{model.table_name}:\n")

for col_name, col_type in Generator.get_date_cols(model.get_all_columns()):
    print(f"{col_name} -> {col_type}")

dt_column_name = cmd.get_item(ID_COL)
id_column_name = cmd.get_item(DATE_TIME_COL)

id_col = model.get_column(dt_column_name)
dt_col = model.get_column(id_column_name)

session = resource.get_session()

min_max_date = session.query(
    func.min(dt_col),
    func.max(dt_col),
    func.count(id_col), )

(min_date, max_date, date_count) = min_max_date.first()

print(min_max_date)
print(f"{dt_column_name}: {min_date} - {max_date} ({date_count})")

# TODO doimplementovat !!!
