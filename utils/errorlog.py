"""
    Použití: vypíše zadaný počet řádek error logu v human-readable formátu.
"""


import os

from classes.env import Env

path = Env.get('webLogs')

log_file = 'error.log'
length = 1

logs = os.popen('tail -n ' + str(length) + ' ' + path + '/' + log_file).read()

lines = logs.split('\\n')

for i in range(0, len(lines)):
    print(lines[i])

headers = lines[0].split(': ')

for i in range(0, len(headers)):
    print(headers[i])
