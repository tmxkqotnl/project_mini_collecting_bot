from math import factorial
from typing import Optional

from src.db.db import Session
from src.models.facility import Facility
from src.common.common import error_handler


@error_handler
def insert_facility(facility: dict[str, Optional[str]]):
    if facility["inst_code"] is None:
        # logging
        raise ValueError("자료 부족 facility")

    for k, v in facility.items():
        if v is None or len(v) == 0:
            facility[k] = None

    with Session() as session:
        new_tr = Facility(**facility)
        fs = (
            session.query(Facility)
            .filter(
                Facility.name == facility["name"],
                Facility.inst_code == facility["inst_code"],
            )
            .all()
        )
        if len(fs) == 0:
            session.add(new_tr)
        session.commit()
