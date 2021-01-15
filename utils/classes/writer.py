import os
import sys


class Writer:

    # TODO: přesunout výpis do standardního vstupu do nové třídy

    _DEST_BASE_FOLDER = 'tmp'

    def __init__(self, subfolder: str) -> None:
        self.__dest_folder = os.path.dirname(os.path.realpath(sys.argv[0])) + '/' + Writer._DEST_BASE_FOLDER
        self.__subfolder = self.__dest_folder + '/' + Writer.get_clean_path(subfolder)

        i = 0
        file_path = f"{self.__subfolder}-{str(i)}.csv"

        while os.path.exists(file_path):
            i += 1
            file_path = f"{self.__subfolder}-{str(i)}.csv"

        self.__temp_file_path = file_path

    @property
    def temp_file_path(self) -> str:
        return self.__temp_file_path

    @property
    def subfolder(self) -> str:
        return self.__subfolder

    @property
    def dest_folder(self) -> str:
        return self.__dest_folder

    def write_temp_file(self, pair_header: (str, str), pair_list: list):
        with open(self.temp_file_path, 'w+') as fw:
            fw.write(f'{pair_header[0]}:{pair_header[1]}\n')

            for fk in pair_list:
                fw.write(f'{fk[0]}:{fk[1]}\n')

    @classmethod
    def get_clean_path(cls, path: str) -> str:
        return path.replace('\\', '/').rstrip('/')
