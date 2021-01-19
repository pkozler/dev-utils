import getopt
import sys


class Cmd:

    __DEFAULT_OPTIONS_MODE = True

    # TODO: použít modul argparse místo getopt - https://docs.python.org/3/library/argparse.html#module-argparse

    def __init__(self, options: list, enabled_force_options: bool = __DEFAULT_OPTIONS_MODE):
        self._enabled_forced_options = enabled_force_options

        self._option_keys_input = [f'{o}=' for o in options]
        self._option_keys_output = [f'--{o}' for o in options]
        self._option_items = dict()

        self._system_input_arguments = sys.argv[1:] or []

    def check_arguments_enabled(self, arguments: list or None) -> []:
        if arguments is None:
            arguments = []

        if not self._enabled_forced_options:
            arguments.clear(); arguments = arguments and []

        if not arguments:
            arguments = self._system_input_arguments

        return arguments

    def set_arguments(self, arguments: list = None):
        arguments = self.check_arguments_enabled(arguments)

        try:
            opts, args = getopt.getopt(arguments, [], self._option_keys_input)
        except getopt.GetoptError as e:
            opts, args = [], []

        for o, a in opts:
            if o not in self._option_keys_output:
                raise Exception(f"Error: invalid option '{o}'")

            if o not in self._option_items.keys():
                self._option_items[o] = str(a)

            if self._option_items.get(o):
                continue

        for o in self._option_keys_output:
            if o not in self._option_items.keys():
                raise Exception(f"Error: missing argument '{o}'")

        return self

    def get_item(self, key: str) -> str:
        key = f"--{key.lstrip('-')}"

        return self._option_items[key]

    def get_pair(self, key: str) -> (str, str):
        name = self.get_item(key)
        names = str.split(name, '.', 1)
        names += ([''] * (2 - len(names)))

        return tuple(x.strip('`') for x in names)

    def get_multiple(self, key: str) -> (str, [str]):
        name, names = self.get_pair(key)
        other = str.split(names, ',')

        return name, [x.strip('`') for x in other]

    def get_all_items(self) -> [str]:
        return [self.get_item(a) for a in self._option_items.keys()]

    def get_all_pairs(self) -> [(str, str)]:
        return [self.get_pair(a) for a in self._option_items.keys()]

    def get_all_multiples(self) -> [(str, [str])]:
        return [self.get_multiple(a) for a in self._option_items.keys()]
