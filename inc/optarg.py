from sqlalchemy import Column, Table

from classes import db
from classes.util import to_prefixed, to_camel_case, get_tab_col
from db.models import Base as Entity

import db.models
import getopt


def get_entity_field(a: str) -> (Entity or Table, Column):
    (tab, col) = get_tab_col(a)
    print(f'column: {tab}.{col}')

    is_class = hasattr(db.models, to_camel_case(tab))
    is_table = hasattr(db.models, to_prefixed(tab))

    if not (is_class or is_table):
        raise Exception(f"Error: invalid table {tab}")

    entity = getattr(db.models, to_camel_case(tab)) if is_class else getattr(db.models, to_prefixed(tab))
    is_field = hasattr(entity, col)

    if not is_field:
        raise Exception(f"Error: invalid column '{tab}.{col}'")

    field = getattr(entity, col)

    return entity, field


def get_pk_fk(args: []) -> (Entity or Table, Column, Entity or Table, Column):
    opts, args = getopt.getopt(args, [], ['fkcol=', 'pkcol='])

    valid_opts = {'--pkcol': (None, None), '--fkcol': (None, None)}
    valid_opts_keys = list(valid_opts.keys())

    for o, a in opts:
        if o not in valid_opts_keys:
            raise Exception(f"Error: invalid option '{o}'")

        for vk in valid_opts_keys:
            if o != vk:
                continue

            entity, field = get_entity_field(a)
            valid_opts[vk] = (entity, field)

            break

    return tuple([value for v in valid_opts.values() for value in v])
