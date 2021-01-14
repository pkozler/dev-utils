"""
    Použití: nalezne přibližný maximální počet záznamů
    k načtení jedním dotazem v zadaném časovém limitu.
"""


import time

from classes.env import Env
from classes.cmd import Cmd
from classes.format import Format

import pymysql.cursors

TABLE, ID_COL, DATE_COL, TIMEOUT = 'table', 'id-col', 'date-col', 'timeout'
# args = f'--{TABLE} sales_flat_order --{ID_COL} entity_id --{DATE_COL} created_at --{TIMEOUT} 10.0'.split()

db = Env.get('db')
host = db['host'].split(':')

addr, port = str(host[0]), int(host[1])

connection = pymysql.connect(host=addr,
                             port=port,
                             user=db['username'],
                             password=db['password'],
                             db=db['dbname'],
                             charset='utf8',
                             cursorclass=pymysql.cursors.DictCursor)

cmd = Cmd([TABLE, ID_COL, DATE_COL, TIMEOUT])
cmd.set_args()

table = cmd.get_item(TABLE).strip('`')
id_col = cmd.get_item(ID_COL).strip('`')
date_col = cmd.get_item(DATE_COL).strip('`')
timeout = float(cmd.get_item(TIMEOUT)) * 1000.0

print(f"{table}.{id_col}, {date_col} -> {timeout} ms\n")


try:
    sql = f"SELECT SQL_NO_CACHE * FROM `{table}` ORDER BY `{id_col}` LIMIT %(limit)s;"

    max_time = 0.0
    last_limit = 0
    current_limit = 1

    while max_time <= timeout:
        params = dict(limit=current_limit)

        with connection.cursor() as cursor:
            Format.print(f'SQL:\n{cursor.mogrify(sql, params)}\n')

            Format.print_info(f'Executing for {current_limit} rows...', bold=True)

            start_time = time.time()
            cursor.execute(sql, params)
            end_time = time.time()

            current_time = (end_time - start_time) * 1000.0

            if current_time > max_time:
                max_time = current_time

            Format.print_info(f'Elapsed time: {current_time} ms', bold=True)

        last_limit = current_limit
        current_limit *= 2

    Format.print_danger(f'Exceeded time limit ({timeout} ms) with {last_limit} rows!', bold=True)

    # TODO: dodatečně zpřesnit pro nalezení optimálního počtu!
finally:
    connection.close()

# TODO: Spočítat min, max, avg, atd. počtu záznamů v tabulce za 1 den, měsíc, rok...
