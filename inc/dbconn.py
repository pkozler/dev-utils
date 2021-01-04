from math import sqrt, ceil

from sqlalchemy.orm import Session


def update_db_records(session: Session, models: (), id_list: [], update_list: []) -> None:
    entity, id_field, update_field = models if (len(models) >= 3) else (None, None, None)

    total_size = len(id_list)
    batch_size = int(round(sqrt(float(total_size))))

    print(f"Total items: {total_size} ({batch_size} per batch)\n")
    last_cnt = 0
    fail_cnt = 0

    for idx, val in enumerate(id_list):
        session.query(entity).filter(id_field == id_list[idx]).update(
            {update_field: update_list[idx]})

        if (idx + 1) % batch_size:
            continue

        try:
            session.commit()
            print(f"Saved #{last_cnt} -> #{idx}")
            last_cnt = idx

        except IndexError as e:
            print(f"Error: *** {e} ***")
            fail_cnt += 1

    try:
        session.commit()
        print(f"Saved #{last_cnt} -> #{total_size}")
    except IndexError as e:
        print(f"Error: *** {e} ***")
        fail_cnt += 1

    print(f"Done. ({int(ceil(float(total_size) / float(batch_size)))} batches, {fail_cnt} failed)")
