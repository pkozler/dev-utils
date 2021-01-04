import os
import json


class Env:

    _CONFIG_FILE_NAME: str = '.env.json'  # _CONFIG_FILE_NAME = 'local.env.json'

    (_config_file_path, _config_data_dict, _config_data_keys) = (None, None, None)

    _config_load_flag: bool = False

    @classmethod
    def _set_loaded(cls, result: ()):
        config_attr_count = len([cls._config_file_path, cls._config_data_dict, cls._config_data_keys])

        if config_attr_count != len(result):
            return

        (config_path, config_data, config_keys) = result

        if not (isinstance(config_path, str) and isinstance(config_data, dict) and isinstance(config_keys, list)):
            return

        cls._config_load_flag = True

        (cls._config_file_path, cls._config_data_dict, cls._config_data_keys) = (config_path, config_data, config_keys)

    @classmethod
    def _is_loaded(cls) -> bool:
        return cls._config_load_flag and (None not in [
            cls._config_file_path, cls._config_data_dict, cls._config_data_keys])

    @classmethod
    def _load(cls, config_name: str = _CONFIG_FILE_NAME) -> ():
        config_path = '' if (not config_name) else (
                os.path.dirname(os.path.realpath(__file__)) + '/../' + config_name)

        if not config_path:
            return ()

        with open(config_path) as config_file:
            raw_config_data = json.load(config_file) or {}

        config_data = {k: v for (k, v) in raw_config_data.items() if (v is not None)}

        if not config_data:
            return ()

        config_keys = list(config_data.keys())

        if not config_keys:
            return ()

        return config_path, config_data, config_keys,

    @classmethod
    def has(cls, key: str) -> bool:
        return cls.get(key) is not None

    @classmethod
    def get(cls, key: str):
        if not cls._is_loaded():
            cls._set_loaded(cls._load())

        if key in cls._config_data_keys:
            return cls._config_data_dict[key]

        return None
