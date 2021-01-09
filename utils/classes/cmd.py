import getopt
import sys


class Cmd:

    def __init__(self, options: list, require: bool = True):
        self._require = require
        self._option_keys_input = [f'{o}=' for o in options]
        self._option_keys_output = [f'--{o}' for o in options]

        self._option_items = dict()

    def set_args(self, arguments: list = None):
        if arguments is None:
            arguments = sys.argv[1:]

        try:
            opts, args = getopt.getopt(arguments, [], self._option_keys_input)
        except getopt.GetoptError as e:
            opts, args = [], []

        for o, a in opts:
            if o not in self._option_keys_output:
                raise Exception(f"Error: invalid option '{o}'")

            if o not in self._option_items.keys():
                self._option_items[o] = str(a).strip()

            if self._option_items.get(o):
                continue

        for o in self._option_keys_output:
            if o in self._option_items.keys():
                continue

            entered = None

            if self._require:
                entered = input(f"Enter '{str(o).lstrip('-')}': ").strip()

            if entered is None:
                raise Exception(f"Error: missing argument '{o}'")

            self._option_items[o] = entered

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
