import os


def get_clean_path(path: str) -> str:
    return path.replace('\\', '/').strip('/')


def get_folder_path(subfolder: str) -> str:
    path = get_clean_path(os.path.realpath(__file__))
    path = get_clean_path(os.path.dirname(path))
    path += ('/../' + get_clean_path(subfolder))

    return '/' + path


def get_temp_file_name(base_path: str, prefix: str) -> str:
    i = 0
    file_path = f"{get_folder_path(base_path)}/{prefix}_{i}.csv"

    while os.path.exists(file_path):
        i += 1
        file_path = f"{get_folder_path(base_path)}/{prefix}_{i}.csv"

    return file_path


def to_prefixed(snake_str: str) -> str:
    return f"t_{snake_str}"


def to_camel_case(snake_str: str) -> str:
    components = snake_str.split('_')

    return components[0].title() + ''.join(x.title() for x in components[1:])


def get_tab_col(arg: str) -> (str, str):
    names = str.split(arg, '.')

    if len(names) <= 1:
        return '', ''

    return names[0], names[1]
