from datetime import datetime
from random import randint


class Generator:
    DEFAULT_MIN_DATE = datetime.strptime("25/12/2011 00:00:00", "%d/%m/%Y %H:%M:%S")
    DEFAULT_MAX_DATE = datetime.strptime("24/12/2020 23:59:59", "%d/%m/%Y %H:%M:%S")

    @classmethod
    def generate_datetime_list(cls, min_date: datetime, max_date: datetime, date_count: int, is_sorted: bool = True) -> []:
        min_timestamp = int(datetime.timestamp(min_date))
        max_timestamp = int(datetime.timestamp(max_date))

        datetime_list = []

        for i in range(date_count):
            random_timestamp = randint(min_timestamp, max_timestamp)
            datetime_list.append(datetime.fromtimestamp(random_timestamp))

        return sorted(datetime_list) if is_sorted else datetime_list

    @classmethod
    def generate_uint_list(cls, key_list: list, uint_count: int, is_sorted: bool = False) -> []:
        uint_list = []

        for i in range(uint_count):
            random_index = randint(1, len(key_list))
            uint_list.append(key_list[random_index])

        return sorted(uint_list) if is_sorted else uint_list
