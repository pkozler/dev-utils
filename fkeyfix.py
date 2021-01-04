"""
    SELECT COUNT(*) FROM aiti_expedition_parcel WHERE flat_order_id NOT IN (SELECT entity_id FROM sales_flat_order);
"""

from sqlalchemy import Column, Table
from sqlalchemy.orm import Query
from sqlalchemy.sql.functions import func

from classes.db import Db as Resource

import db.models
from classes.generator import Generator
from classes.util import get_temp_file_name
from db.models import Base as Entity

from inc import optarg
import inc.tempfile as Cache
import inc.dbconn as Model

args = '--fkcol aiti_expedition_parcel.flat_order_id --pkcol sales_flat_order.entity_id'.split()
# args = sys.argv[1:]

Resource = Resource.connect(env_db=Resource.db_vyvojar_localhost)

# Init:

(fields): (Entity or Table, Column, Entity or Table, Column) = optarg.get_pk_fk(args)
pk_entity, pk_field, fk_entity, fk_field = fields
fk_pk_field: Column = list(fk_field.table.primary_key.columns)[0]  # TODO multiple primary key columns!

print(f'\n{fk_entity}.{fk_pk_field} :: {fk_entity}.{fk_field} -> {pk_entity}.{pk_field}')

# Main:

session = Resource.get_session()

query_pk: Query = session.query(pk_field)
query_cnt_fk: Query = session.query(func.count(fk_pk_field))
query_fk_not_in: Query = session.query(fk_pk_field, fk_field).filter(
    fk_field.notin_(query_pk.subquery())).order_by(fk_pk_field)

print(f'Loading key column values from database:\n"{query_fk_not_in}\n"')

pk_list: list = query_pk.all()
pk_cnt: int = len(pk_list)
print(f'Loaded {pk_cnt} rows for {pk_field.table} PK {pk_field}...')

fk_broken_list: list = query_fk_not_in.all()
fk_broken_cnt: int = len(fk_broken_list)
print(f'Loaded {fk_broken_cnt} rows for {fk_field.table} broken FK {pk_field} ordered by p_key {fk_pk_field}...')

fk_cnt: int = int(query_cnt_fk.first()[0])
broken_to_cnt: float = float(fk_broken_cnt) / float(fk_cnt)
print(f'Broken keys: {fk_broken_cnt} from {fk_cnt} ({100.0 * round(broken_to_cnt, 4)} %)')

temp_file = get_temp_file_name('temp', Resource.dbname)
print(f'Writing current state into temporary file:\n"{temp_file}"')
input("Enter to proceed: ")

Cache.write_temp_file(temp_file, fk_field, fk_pk_field, fk_broken_list)

print(f'Generating new keys to {pk_field} from {fk_field} for each {fk_pk_field}:')
pk_val_list = [pk[0] for pk in pk_list]
new_fk_list = Generator.generate_uint_list(pk_val_list, fk_broken_cnt, True)
new_fk_cnt = len(new_fk_list)

if new_fk_cnt != fk_broken_cnt:
    print(f'Failed with generation of {new_fk_cnt} keys instead of {fk_broken_cnt} required!')
    exit(1)

print(f'Completed generation of required {fk_broken_cnt} keys.')

fk_id_list = [fk[0] for fk in fk_broken_list]

print(f'Saving changes into database:\n"{Resource.dbname}"')
input("Enter to proceed: ")

Model.update_db_records(session, (fk_entity, fk_pk_field, fk_field), fk_id_list, new_fk_list)

print(f'All updates finished: proceeding to final check of the results...')

query_cnt_fk_not_in_check: Query = session.query(func.count(fk_pk_field)).filter(
    fk_field.notin_(session.query(pk_field).subquery()))
final_results_check = int(query_cnt_fk_not_in_check.first()[0])

if final_results_check:
    print(f'{final_results_check} broken foreign keys found in "{fk_field}" - the operation has failed!\n')
    exit(1)

print(f'{final_results_check} broken foreign keys found in "{fk_field}" - the operation was successful.\n')
