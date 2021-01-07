from math import sqrt, ceil
from sqlalchemy import Column, Table

from sqlalchemy.orm import Session
from db.models import Base as Entity


class Connection:

    def __init__(self, session: Session, entity: Entity or Table):
        self.__session, self.__entity = session, entity
        self._id_field, self._update_field = None, None
        self._id_list, self._update_list = None, None
        self._total_size = 0
        self._batch_size = 0

    @property
    def session(self) -> Session:
        return self.__session

    @property
    def entity(self) -> Entity or Table:
        return self.__entity

    def set_db_fields(self, id_field: Column, update_field: Column, id_list: [], update_list: []) -> ():
        self._id_field, self._update_field = id_field, update_field
        self._id_list, self._update_list = id_list, update_list

        self._total_size = len(id_list)
        self._batch_size = int(round(sqrt(float(self._total_size))))

        return self._total_size, self._batch_size

    def update_db_records(self) -> ():
        last_cnt = 0
        fail_cnt = 0

        for idx, val in enumerate(self._id_list):
            self.session.query(self.entity).filter(self._id_field == self._id_list[idx]).update(
                {self._update_field: self._update_list[idx]})

            if (idx + 1) % self._batch_size:
                continue

            try:
                self.session.commit()
                # print(f"Saved #{last_cnt} -> #{idx}")
                last_cnt = idx

            except IndexError as e:
                # print(f"Error: *** {e} ***")
                fail_cnt += 1

        try:
            self.session.commit()
            print(f"Saved #{last_cnt} -> #{self._total_size}")
        except IndexError as e:
            print(f"Error: *** {e} ***")
            fail_cnt += 1

        batch_cnt = int(ceil(float(self._total_size) / float(self._batch_size)))

        return batch_cnt, fail_cnt
