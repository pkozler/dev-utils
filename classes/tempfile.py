import os


class TempFile:

    def __init__(self, base_path: str, prefix: str) -> None:
        self.__prefix = prefix

        path = self.get_clean_path(os.path.realpath(__file__))
        path = self.get_clean_path(os.path.dirname(path))
        path += ('/../' + self.get_clean_path(base_path))

        self.__subfolder = ('/' + path)

        i = 0
        file_path = f"{self.__subfolder}/{self.__prefix}_{i}.csv"

        while os.path.exists(file_path):
            i += 1
            file_path = f"{self.__subfolder}/{self.__prefix}_{i}.csv"

        self.__temp_file_path = file_path

    @property
    def temp_file_path(self) -> str:
        return self.__temp_file_path

    @property
    def subfolder(self) -> str:
        return self.__subfolder

    @property
    def prefix(self) -> str:
        return self.__prefix

    def write_temp_file(self, pair_header: (str, str), pair_list: list):
        with open(self.temp_file_path, 'w+') as fw:
            fw.write(f'{pair_header[0]:{pair_header[1]}}\n')

            for fk in pair_list:
                fw.write(f'{fk[0]}:{fk[1]}\n')

    @classmethod
    def get_clean_path(cls, path: str) -> str:
        return path.replace('\\', '/').strip('/')
