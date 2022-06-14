from typing import Optional
from sqlalchemy.orm.exc import NoResultFound
from src.db.db import Session
from src.models.facility import Facility
from src.common.common import error_handler


@error_handler
def insert_facility(facility: dict[str, Optional[str]]):
    # 테스트 후 삭제
    if facility["inst_code"] is None:
        raise ValueError("자료 부족 facility")

    for k, v in facility.items():
        if v is None or len(v) == 0:
            facility[k] = None

    with Session() as session:
        new_tr = Facility(**facility)
        try:
            fs = (
                session.query(Facility)
                .filter(
                    Facility.name == facility["name"],
                    Facility.inst_code == facility["inst_code"],
                    Facility.tr_id == facility["tr_id"],
                    Facility.degree == facility["degree"],
                )
                .one()
            )
            session.query(Facility).filter(Facility.id == fs.id).update(facility)
        except NoResultFound:
            session.add(new_tr)

        session.commit()
