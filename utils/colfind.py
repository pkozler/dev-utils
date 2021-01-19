"""
    Použití: prohledá všechny sloupce ve všech tabulkách a vypíše dvojici ve formátu
    'tabulka.sloupec', pro všechny sloupce, jejichž název obsahuje zadaný podřetězec.
"""


import pymysql.cursors
from pymysql import Connection

from classes.cmd import Cmd
from classes.env import Env
from classes.format import Format


OPT_SEARCH = 'search'


def get_clean_identifier(substr: str) -> str or None:
    identifier = substr.strip().strip('`')

    if not len(identifier):
        return None

    return identifier


def get_db_name(db_conf: dict) -> str or None:
    if 'dbname' not in db_conf.keys():
        return None

    return get_clean_identifier(db_conf['dbname'])


def get_db_conn(db_conf: dict) -> Connection or None:
    try:
        host_port = db_conf['host'].split(':')

        if len(host_port) <= 0:
            return None

        db_host = host_port[0]

        if len(host_port) <= 1:
            return pymysql.connect(host=db_host,
                                   user=db_conf['username'],
                                   password=db_conf['password'],
                                   db='information_schema',
                                   charset='utf8',
                                   cursorclass=pymysql.cursors.DictCursor)

        db_port = int(host_port[1])

        return pymysql.connect(host=db_host,
                               port=db_port,
                               user=db_conf['username'],
                               password=db_conf['password'],
                               db='information_schema',
                               charset='utf8',
                               cursorclass=pymysql.cursors.DictCursor)

    except Exception as e:

        print(e)
        exit(1)
        return None


def print_search_result(connection: Connection, db_name: str, search_str: str):
    try:
        with connection.cursor() as cursor:
            sql = """SELECT `table_schema`, `table_name`, `column_name` 
                        FROM `columns` 
                        WHERE `table_schema` = \'{}\' 
                        AND `column_name` LIKE \'%{}%\' 
                        ORDER BY `table_schema`, `table_name`, `column_name`
                        ;""".format(db_name, search_str)

            Format.print()

            Format.print('Query:', bold=True)
            Format.print(sql + '\n')

            cursor.execute(sql)
            result = cursor.fetchall()

            Format.print_success('Results:', bold=True)

            for row in result:
                Format.print_success("{}.{}".format(row['table_name'], row['column_name']))

    except Exception as e:
        Format.print_danger('Error:\n' + str(e))
    finally:
        connection.close()


def search_table_columns(db_conf: dict, search_str: str):
    if search_str is None:
        Format.print_info('No search string...')

        return

    db_name = get_db_name(db_conf)

    if db_name is None:
        Format.print_warning('Cannot find dbname.')

        return

    connection = get_db_conn(db_conf)

    if connection is None:
        Format.print_danger('DB connection failed!')

        return

    print_search_result(connection, db_name, search_str)


config = Env.get('db')
cmd = Cmd([OPT_SEARCH])

search = get_clean_identifier(cmd.set_arguments().get_item(OPT_SEARCH))
search_table_columns(config, search)
