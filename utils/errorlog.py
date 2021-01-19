"""
    Použití: vypíše zadaný počet řádek error logu v human-readable formátu.
"""


import os

from classes.cmd import Cmd
from classes.env import Env
from classes.format import Format
from classes.writer import Writer


OPT_LINES = 'count'


def try_get_int(val: str) -> int:
    try:
        v = int(val)

        return v
    except ValueError:
        return 0


def print_log_header(header: str):
    tokens = header.split(' ')

    if not len(tokens):
        return

    Format.print_danger(' | '.join([t.strip('[]') for t in tokens]), bold=True)


def print_log_lines(lines: [str]):
    if not len(lines):
        Format.print()

        return

    for line in range(len(lines)):
        Format.print(lines[line])


def print_logs(size: int, logs: str):
    Format.print("Count: {}\n".format(str(size)))

    if not size:
        return

    lines = logs.split('\n')

    for line in lines:
        tokens = line.split(': ')

        if len(tokens) <= 0:
            continue

        print_log_header(tokens[0])

        if len(tokens) <= 1:
            continue

        print_log_lines(tokens[1:])

        Format.print()


path = Env.get('webLogs')
log_file = Writer.get_clean_path(str(path)) + '/' + 'error.log'

cmd = Cmd([OPT_LINES])
line_cnt = try_get_int(cmd.set_arguments().get_item(OPT_LINES))

logs_str = os.popen('tail -n ' + str(line_cnt) + ' ' + log_file).read()
print_logs(line_cnt, logs_str)
