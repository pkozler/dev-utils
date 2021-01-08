from math import sqrt, ceil
from sqlalchemy import Column, Table

from sqlalchemy.orm import Session
from utils.db.models import Base as Entity


class Connection:

    def __init__(self, session: Session, entity: Entity or Table, id_field: Column, update_field: Column):
        self.__session, self.__entity = session, entity
        self._id_field, self._update_field = id_field, update_field

        self._id_list, self._update_list = [], []
        self._total_size, self._batch_size = 0, 0

    @property
    def session(self) -> Session:
        return self.__session

    @property
    def entity(self) -> Entity or Table:
        return self.__entity

    def set_db_fields(self, id_list: [], update_list: []) -> ():
        self._id_list, self._update_list = id_list, update_list

        self._total_size = len(id_list)
        self._batch_size = int(round(sqrt(float(self._total_size))))
        batch_cnt = int(ceil(float(self._total_size) / float(self._batch_size)))

        return self._total_size, self._batch_size, batch_cnt

    def update_db_records(self) -> ():
        last_cnt = 0

        for idx, val in enumerate(self._id_list):
            self.session.query(self.entity).filter(self._id_field == val).update(
                {self._update_field: self._update_list[idx]})

            if (idx + 1) % self._batch_size:
                continue

            self.session.commit()

            yield last_cnt, idx

            last_cnt = idx + 1

        self.session.commit()

        yield last_cnt, self._total_size
