from typing import Optional

from src.db.db import Session
from src.models.equipment import Equipment
from src.common.common import error_handler


@error_handler
def insert_equipment(equipment: dict[str, Optional[str]]):
    if equipment["inst_code"] is None:
        # logging
        raise ValueError("자료 부족 equipment")

    for k, v in equipment.items():
        if v is None or len(v) == 0:
            equipment[k] = None

    with Session() as session:
        new_tr = Equipment(**equipment)
        es = (
            session.query(Equipment)
            .filter(
                Equipment.name == equipment["name"],
                Equipment.inst_code == equipment["inst_code"],
            )
            .all()
        )
        if len(es) == 0:
            session.add(new_tr)
        session.commit()
