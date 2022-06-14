from typing import Optional
from src.models.training import Training
from src.db.db import Session
from src.common.common import error_handler

# base_adrs, base_adrs_detail


def get_training(params: dict[str, str]):
    with Session() as session:
        return session.query(Training).first()


def get_training_cnt():
    with Session() as session:
        return session.query(Training).all().cnt()


@error_handler
def insert_training(tr: dict[str, Optional[str]]):
    if tr["inst_code"] is None or tr["inst_code"] == "":
        # logging
        raise ValueError("자료 부족 training")

    for k, v in tr.items():
        if v is None or len(v) == 0:
            tr[k] = None

    with Session() as session:
        new_tr = Training(**tr)
        trs = (
            session.query(Training)
            .filter(Training.tr_id == tr["tr_id"], Training.degree == tr["degree"])
            .all()
        )
        if len(trs) == 0:
            session.add(new_tr)
        session.commit()
