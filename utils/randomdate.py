"""
    Použití: v tabulce např. sales_flat_order nastaví hodnoty created_at náhodně
    z intervalu '2012-01-01' až '2020-12-31', aby pro záznamy X a Y platilo,
    že pokud  X.entity_id  < Y.entity_id , pak i X.created_at < Y.created_at"
    (typický problém při testování BI metrik, kde chceme mít zdrojová data
    ideálně z několika let nazpátek, ale pro úsporu místa máme na devu data
    jen za několik posledních měsíců).
"""

from sqlalchemy import func

from classes.model import Model
from classes.updater import Updater
from classes.generator import Generator
from classes.resource import Resource
from classes.cmd import Cmd

TABLE, ID_COL, DATE_TIME_COL = 'table', 'idcol', 'dtcol'
# args = '--table sales_flat_order --idcol entity_id --dtcol created_at'.split()
# args = '--table aiti_expedition_tracking_number --idcol tracking_id --dtcol reimported_at'.split()

resource = Resource.connect()
cmd = Cmd([TABLE, ID_COL, DATE_TIME_COL])

table = cmd.set_args().get_item(TABLE)
model = Model(resource, table)

print(f"{model.table_name}:\n")

for col_name, col_type in Generator.get_date_cols(model.get_all_columns()):
    print(f"{col_name} -> {col_type}")

id_column_name = cmd.get_item(ID_COL)
dt_column_name = cmd.get_item(DATE_TIME_COL)

id_col = model.get_column(id_column_name)
dt_col = model.get_column(dt_column_name)

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

# input("Enter to proceed: ")
updater = Updater(session, model, id_column_name, dt_column_name)

total_size, batch_size, batch_cnt = updater.set_db_fields(
    [i[0] for i in id_list], datetime_list)

if total_size != len(datetime_list):
    print(f'Error: id_list_size <> dt_list_size!')
    exit(1)

print(f"Total items: {total_size} ({batch_size} per batch)\n")

counter = 0

try:
    for x0, x1 in updater.update_db_records():
        print(f"Saved #{x0} -> #{x1}")
        counter += 1

except IndexError as e:
    print(f"Error:\n{str(e)}\n")

print(f"Done. ({counter} from {batch_cnt} batches)")
