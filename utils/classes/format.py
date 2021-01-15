class Format:

    # TODO: vracení výstupu namísto výpisu (přesunout do nové třídy pro logování)

    COLOR = dict(
        primary=95,
        info=94,
        success=92,
        warning=93,
        danger=91,
    )

    STYLE = dict(
        bold=1,
        underline=4,
    )

    RESET = 0

    @classmethod
    def _print(cls, text, bold, underline, coloring):
        if bold and underline:
            style = ';'.join([str(cls.STYLE['bold']), str(cls.STYLE['underline'])])
        elif bold:
            style = str(cls.STYLE['bold'])
        elif underline:
            style = str(cls.STYLE['underline'])
        else:
            style = None

        if coloring in cls.COLOR.values():
            color = str(coloring)
        else:
            color = None

        if (color is not None) and (style is not None):
            formatting = ';'.join([style, color])
        elif (color is not None) or (style is not None):
            formatting = str(color) if (style is None) else str(style)
        else:
            formatting = None

        if formatting is not None:
            print('\033[{}m{}\033[{}m'.format(formatting, str(text), str(cls.RESET)))
        else:
            print(str(text))

    @classmethod
    def print(cls, text='', bold=False, underline=False):
        cls._print(text, bold, underline, None)
        return cls

    @classmethod
    def print_primary(cls, text='', bold=False, underline=False):
        cls._print(text, bold, underline, cls.COLOR['primary'])
        return cls

    @classmethod
    def print_info(cls, text='', bold=False, underline=False):
        cls._print(text, bold, underline, cls.COLOR['info'])
        return cls

    @classmethod
    def print_success(cls, text='', bold=False, underline=False):
        cls._print(text, bold, underline, cls.COLOR['success'])
        return cls

    @classmethod
    def print_warning(cls, text='', bold=False, underline=False):
        cls._print(text, bold, underline, cls.COLOR['warning'])
        return cls

    @classmethod
    def print_danger(cls, text='', bold=False, underline=False):
        cls._print(text, bold, underline, cls.COLOR['danger'])
        return cls
