from typing import Optional
from sqlalchemy.orm.exc import NoResultFound
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
    # 테스트 후 삭제
    if tr["inst_code"] is None or tr["inst_code"] == "":
        raise ValueError("자료 부족 training")

    for k, v in tr.items():
        if v is None or len(v) == 0:
            tr[k] = None

    with Session() as session:
        new_tr = Training(**tr)
        try:
            trs = (
                session.query(Training)
                .filter(Training.tr_id == tr["tr_id"], Training.degree == tr["degree"])
                .one()
            )
            session.query(Training).filter(Training.id == trs.id).update(Training)
        except NoResultFound as e:
            session.add(new_tr)

        session.commit()
