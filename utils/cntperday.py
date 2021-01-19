"""
    Použití: nalezne přibližný maximální počet záznamů
    k načtení jedním dotazem v zadaném časovém limitu.
"""


import time

from classes.env import Env
from classes.cmd import Cmd
from classes.format import Format

import pymysql.cursors


OPTS = TABLE, ID_COL, DATE_COL, TIMEOUT = 'table', 'id-col', 'date-col', 'timeout'
cmd = Cmd([TABLE, ID_COL, DATE_COL, TIMEOUT])
cmd.set_arguments(f'--{TABLE} sales_flat_order --{ID_COL} entity_id --{DATE_COL} created_at --{TIMEOUT} 5.0'.split())


def create_connection():
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

    table = cmd.get_item(TABLE).strip('`')
    id_col = cmd.get_item(ID_COL).strip('`')
    date_col = cmd.get_item(DATE_COL).strip('`')
    timeout = float(cmd.get_item(TIMEOUT)) * 1000.0

    print(f"{table}.{id_col}, {date_col} -> limit {timeout / 1000.0} seconds\n")

    return connection, table, id_col, date_col, timeout,

def find_max_limit():
    connection, table, id_col, date_col, timeout = create_connection()

    try:
        sql = f"SELECT SQL_NO_CACHE * FROM `{table}` ORDER BY `{id_col}` LIMIT %(limit)s;"

        max_time = 0.0
        last_limit = 0
        current_limit = 1

        # TODO přepočítávat koeficient násobení podle rozdílu časů

        while max_time <= timeout:
            params = dict(limit=current_limit)
            Format.print(f'SQL:\n{cursor.mogrify(sql, params)}\n')

            with connection.cursor() as cursor:
                Format.print_info(f'Executing for {current_limit} rows...', bold=True)

                start_time = time.time()
                cursor.execute(sql, params)
                end_time = time.time()

                current_time = (end_time - start_time) * 1000.0

                if current_time > max_time:
                    next_max_time = current_time

                time_diff = next_max_time - max_time
                Format.print_info(f'Elapsed time: {next_max_time} ms (+ {time_diff})', bold=True)

            last_limit = current_limit
            current_limit *= 2

        current_limit = last_limit
        last_limit /= 2

        Format.print_danger(f'Exceeded time limit ({timeout} ms) with {last_limit} rows!', bold=True)
    finally:
        connection.close()


find_max_limit()

# TODO: Spočítat min, max, avg, atd. počtu záznamů v tabulce za 1 den, měsíc, rok...
