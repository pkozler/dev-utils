import random
import string

from jinja2 import Template


class Initializer:
    # initial values:

    (_default_dev_vhost_id, _default_dev_username_prefix, _default_vhost_url_domain,
     _default_dir_www, _default_subdir_log, _default_subdir_web) = (
        13, 'vyvojar%d', 'tmp123.cz', '/var/www', 'web', 'logs')

    (_default_host_address, _default_port_number, _default_dev_alt_username,
     _default_random_string_length, _default_password_hide_char, _default_dev_alt_dbname) = (
        ('localhost', '127.0.0.1'), 3306, 'developer', 16, '*', 'pz_dev')

    (_default_char_set, _default_db_init_statements,
     _default_db_model, _default_db_type, _default_db_active) = (
        'utf8', 'SET NAMES %s', 'mysql4', 'pdo_mysql', 1)

    # config keys:

    _DB_CONFIG_KEYS_REQUIRED = __key_host, __key_username, __key_password, __key_dbname, = (
        'host', 'username', 'password', 'dbname',)
    _DB_CONFIG_KEYS_OPTIONAL = __optkey_init_statements, __optkey_model, __optkey_type, __optkey_pdo_type, __optkey_active, = (
        'initStatements', 'model', 'type', 'pdoType', 'active',)

    # formatted values:

    _DB_CONFIG_VALUES_REQUIRED = [
        ':'.join([str(_default_host_address[1]), str(_default_port_number)]),
        _default_dev_alt_username,
        str(_default_password_hide_char * _default_random_string_length),
        _default_dev_alt_dbname,
    ]

    _DB_CONFIG_VALUES_OPTIONAL = [
        (_default_db_init_statements % _default_char_set),
        _default_db_model,
        _default_db_type,
        '',
        _default_db_active,
    ]

    # initializing methods:

    def __init__(self, vh_id: int = _default_dev_vhost_id) -> None:
        self._username = (Initializer._default_dev_username_prefix % vh_id)
        self._server_root_url = '.'.join([self._username, Initializer._default_vhost_url_domain])

        self.__path_web = self.build_work_dir_path(Initializer._default_subdir_web)
        self.__path_log = self.build_work_dir_path(Initializer._default_subdir_log)

        self._config_keys = [Initializer._DB_CONFIG_KEYS_REQUIRED + Initializer._DB_CONFIG_KEYS_OPTIONAL]
        self.__db_local, self.__db_image = dict.fromkeys(self._config_keys), dict.fromkeys(self._config_keys)


    # TODO: načtení specifických hodnot konfigurací DB přes dialogy v příkazové řádce


    @property
    def path_web(self):
        return self.__path_web

    @property
    def path_log(self):
        return self.__path_log

    @property
    def db_local(self):
        return self.__db_local

    @property
    def db_image(self):
        return self.__db_image


    # TODO: výpis hodnot konfigurace do šablony JSON souboru s využitím šablonovacího systému


    def setup_db_config(self, is_localhost: bool, host_ip_port: (str, int) or None) -> dict:
        if is_localhost:
            db_config = self.create_db_config_items(Initializer._default_host_address[0], None)

            for key, val in db_config.items():
                self.db_local[key] = val

            return self.db_local

        if host_ip_port is None:
            host_ip_port: (str, int) = (Initializer._default_host_address[1], Initializer._default_port_number)

        host_addr, host_port = host_ip_port
        db_config = self.create_db_config_items(host_addr, host_port)

        for key, val in db_config.items():
            self.db_image[key] = val

        return self.db_image

    def build_work_dir_path(self, project_root_subdir: str) -> str:
        return '/'.join([Initializer._default_dir_www, self._server_root_url, project_root_subdir])

    def create_db_config_items(self, host_addr: str, host_port: int or None) -> dict:
        localhost = Initializer._default_host_address[0]

        if host_addr == Initializer._default_host_address[1]:
            host_addr = localhost

        if host_port == Initializer._default_port_number:
            host_port = None

        host = ':'.join(
            [host_addr] + ([] if (host_port is None) else [host_port])
        )

        config_keys = [Initializer._DB_CONFIG_KEYS_REQUIRED + Initializer._DB_CONFIG_KEYS_OPTIONAL]

        if host == localhost:
            username, dbname = self._username, self._username
            password = self.generate_random_string()

            config_vals = [host, username, password, dbname] + Initializer._DB_CONFIG_VALUES_OPTIONAL
        else:
            config_vals = Initializer._DB_CONFIG_VALUES_REQUIRED + Initializer._DB_CONFIG_VALUES_OPTIONAL

        return dict(zip(config_keys, config_vals))

    def generate_random_string(self, length: int = _default_random_string_length,
                               placeholder: str = _default_password_hide_char) -> str:
        if not length:
            return self._username

        if placeholder:
            char = str(placeholder[0])

            return char * length

        letters = string.ascii_letters + string.digits

        return ''.join(random.choice(letters) for _ in range(length))
