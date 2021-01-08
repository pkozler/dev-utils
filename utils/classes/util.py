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


def get_clean_path(cls, path: str) -> str:
    return path.replace('\\', '/').strip('/')
