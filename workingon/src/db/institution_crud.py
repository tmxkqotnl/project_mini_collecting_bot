from typing import Optional

from src.db.db import Session
from src.models.institution import Institution
from src.common.common import error_handler


@error_handler
def insert_institution(inst: dict[str, Optional[str]]):
    if inst["inst_code"] is None or inst["inst_code"] == "":
        # logging
        raise ValueError("자료 부족 institution")

    for k, v in inst.items():
        if v is None or len(v) == 0:
            inst[k] = None
    with Session() as session:
        new_tr = Institution(**inst)
        insts = (
            session.query(Institution)
            .filter(Institution.inst_code == inst["inst_code"])
            .all()
        )
        if len(insts) == 0:
            session.add(new_tr)
        session.commit()
