from math import sqrt, ceil
from sqlalchemy import Column, Table

from sqlalchemy.orm import Session

from classes.model import Model
from db.models import Base as Entity


class Updater:

    def __init__(self, session: Session, model: Model, id_field: str, update_field: str):
        self.__session, self.__entity = session, model.entity
        self._id_field, self._update_field = model.get_column(id_field), model.get_column(update_field)

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
        self._batch_size = max([1, int(round(sqrt(float(self._total_size))))])
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
