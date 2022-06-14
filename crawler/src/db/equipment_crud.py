from typing import Optional
from sqlalchemy.orm.exc import NoResultFound
from src.db.db import Session
from src.models.equipment import Equipment
from src.common.common import error_handler


@error_handler
def insert_equipment(equipment: dict[str, Optional[str]]):
    # 테스트 후 삭제
    if equipment["inst_code"] is None:
        raise ValueError("자료 부족 equipment")

    for k, v in equipment.items():
        if v is None or len(v) == 0:
            equipment[k] = None

    with Session() as session:
        new_tr = Equipment(**equipment)
        try:
            es = (
                session.query(Equipment)
                .filter(
                    Equipment.name == equipment["name"],
                    Equipment.inst_code == equipment["inst_code"],
                    Equipment.tr_id == equipment["tr_id"],
                    Equipment.degree == equipment["degree"],
                )
                .one()
            )
            session.query(Equipment).filter(Equipment.id == es.id).update(equipment)
        except NoResultFound as e:
            session.add(new_tr)

        session.commit()
