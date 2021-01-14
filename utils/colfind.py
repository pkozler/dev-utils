"""
    Použití: prohledá všechny sloupce ve všech tabulkách a vypíše dvojici ve formátu
    'tabulka.sloupec', pro všechny sloupce, jejichž název obsahuje zadaný podřetězec.
"""


import pymysql.cursors

from classes.env import Env
from classes.format import Format

config = Env.get('db')

db_name = config['dbname']

connection = pymysql.connect(host=config['host'],
                             user=config['username'],
                             password=config['password'],
                             db='information_schema',
                             charset='utf8',
                             cursorclass=pymysql.cursors.DictCursor)

search_string = input('Search:')

try:
    with connection.cursor() as cursor:
        sql = """SELECT `table_schema`, `table_name`, `column_name` 
        FROM `columns` 
        WHERE `table_schema` = \'{}\' 
        AND `column_name` LIKE \'%{}%\' 
        ORDER BY `table_schema`, `table_name`, `column_name`
        ;""".format(db_name, search_string)

        Format.print()

        Format.print('Query:', bold=True)
        Format.print(sql + '\n')

        cursor.execute(sql)
        result = cursor.fetchall()

        Format.print('Results:', bold=True)

    for row in result:
        Format.print("{}.{}".format(row['table_name'], row['column_name']))

finally:
    connection.close()
