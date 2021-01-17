class Prompt:

    @classmethod
    def prompt_str_value(cls, key_name: str, default_value: str = None) -> str:
        prompt = f'{key_name}: '

        if type(default_value) is str:
            default_value = default_value.strip()
            prompt += f'({default_value}) '
            default_value = default_value or ' '

        value = None

        while value is None:
            value = input(prompt).strip()

            if default_value is not None:
                value = value or default_value

            if not value:
                value = None
        else:
            value = value.strip()
            print(f'{key_name} = "{value}"')

        return value

    @classmethod
    def prompt_int_value(cls, key_name: str, default_value: int = None) -> int:
        prompt = f'{key_name} -> int: '

        if type(default_value) is int:
            prompt += f'({default_value}) '

        value = None

        while value is None:
            value = input(prompt).strip()

            if not value:
                value = default_value

            try:
                value = int(value, 0)
            except ValueError:
                value = None
        else:
            print(f'{key_name} = \t{value}')

        return value

    @classmethod
    def prompt_float_value(cls, key_name: str, default_value: float = None) -> float:
        prompt = f'{key_name} -> float: '

        if type(default_value) is float:
            prompt += f'({default_value}) '

        value = None

        while value is None:
            value = input(prompt).strip()

            if not value:
                value = default_value

            try:
                value = float(value)
            except ValueError:
                value = None
        else:
            print(f'{key_name} ≈ \t{value}')

        return value

    @classmethod
    def prompt_bool_value(cls, key_name: str, default_value: bool = None) -> bool:
        prompt = f'{key_name}? [y/n]: '

        if type(default_value) is bool:
            substr = ('y' if default_value else 'n')
            prompt += f'({substr}) '

        y_values = ['y', 'yes', 'true', 't', '1']
        n_values = ['n', 'no', 'false', 'f', '0']

        value = None

        while value is None:
            value = input(prompt).strip().lower()

            if not value:
                value = default_value
            else:
                if value in y_values:
                    value = True
                elif value in n_values:
                    value = False
                else:
                    value = None
        else:
            print(f'{key_name} = \t{str(value).upper()}')

        return value
