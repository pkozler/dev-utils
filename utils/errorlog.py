"""
    Použití: vypíše zadaný počet řádek error logu v human-readable formátu.
"""


import os

from classes.env import Env
from classes.format import Format
from classes.writer import Writer


def try_get_int(val: str, default: int = 1) -> int:
    try:
        v = int(val)

        return v
    except ValueError:
        return default


def print_log_header(header: str):
    tokens = header.split(' ')

    if not len(tokens):
        return

    Format.print_primary(' | '.join([t.strip('[]') for t in tokens]))


def print_log_lines(lines: [str]):
    if not len(lines):
        Format.print()

        return

    for line in range(len(lines)):
        Format.print_info(lines[line])


def print_logs(size: int, logs: str):
    Format.print("Count: {}".format(str(size)))

    if not size:
        return

    lines = logs.split('\\n')

    for i in range(len(lines)):
        tokens = lines[i].split(': ')

        if len(tokens) <= 0:
            continue

        print_log_header(tokens[0])

        if len(tokens) <= 1:
            continue

        print_log_lines(tokens[1:])


path = Env.get('webLogs')
log_file = Writer.get_clean_path(str(path)) + '/' + 'error.log'

line_cnt = try_get_int(input('Lines:'))

logs_str = os.popen('tail -n ' + str(line_cnt) + ' ' + log_file).read()
print_logs(line_cnt, logs_str)
