from utils.classes.env import Env

from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker, Session
from urllib import parse


class Db:

    DB_ENVIRONMENT_CONFIG_NAMES = (db_vyvojar_localhost, db_pz_dev_img_docker) = ('dbOld', 'db')
    DB_OPTIONAL_CONFIG_DEFAULTS = (db_default_encoding, db_default_is_echo_on) = ('utf8', False)

    def __init__(self, conf: dict, msg_opts: (str, bool)):
        self.__username, self.__dbname, self.__host = conf['username'], conf['host'], conf['dbname']
        self._engine, self._session, self._inspector = None, None, None
        self._table_names = None
        self._loaded_tables = None

        conn_str = 'mysql+pymysql://{}:{}@{}/{}'.format(conf['username'],
                                                        parse.quote_plus(conf['password']),
                                                        conf['host'], conf['dbname'])

        self._config = {'url': conn_str, 'encoding': msg_opts[0], 'echo': msg_opts[1]}

    @property
    def username(self) -> str:
        return self.__username

    @property
    def host(self) -> str:
        return self.__dbname

    @property
    def dbname(self) -> str:
        return self.__host

    def get_engine(self):
        if self._engine is None:
            self._engine = create_engine(self._config['url'],
                                         encoding=self._config['encoding'], echo=self._config['echo'])
            self._engine.connect()

        return self._engine

    def get_session(self) -> Session:
        if self._session is None:
            engine = self.get_engine()
            Session = sessionmaker(bind=engine)
            self._session = Session()

        return self._session

    def get_inspector(self):
        if self._inspector is None:
            engine = self.get_engine()
            self._inspector = inspect(engine)

        return self._inspector

    def get_tables(self) -> dict:
        if self._table_names is None:
            inspector = self.get_inspector()
            self._table_names = inspector.get_table_names(schema=self.dbname)

        return self._table_names

    def has_table(self, table_name: str) -> bool:
        return table_name in self.get_tables()

    def get_table_detail(self, table_name: str):
        if not self.has_table(table_name):
            return None

        if self._loaded_tables is None:
            self._loaded_tables = {}

        if table_name not in self._loaded_tables.keys():
            inspector = self.get_inspector()

            self._loaded_tables[table_name] = dict(
                table_name=table_name,
                columns=inspector.get_columns(table_name, schema=self.dbname),
                pk_constraint=inspector.get_pk_constraint(table_name, schema=self.dbname),
                foreign_keys=inspector.get_foreign_keys(table_name, schema=self.dbname),
                indexes=inspector.get_indexes(table_name, schema=self.dbname),
                unique_constraints=inspector.get_unique_constraints(table_name, schema=self.dbname),
                check_constraints=inspector.get_check_constraints(table_name, schema=self.dbname), )

        return self._loaded_tables.get(table_name) or None

    @classmethod
    def connect(cls, env_db: str = db_pz_dev_img_docker):
        if env_db not in Db.DB_ENVIRONMENT_CONFIG_NAMES:
            return None

        return Db(Env.get(env_db), cls.DB_OPTIONAL_CONFIG_DEFAULTS)
