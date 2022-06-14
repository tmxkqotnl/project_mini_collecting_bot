import uuid
from sqlalchemy import TEXT, Column
from src.db.db import Base
from sqlalchemy.dialects.postgresql import UUID

# fix - type fix
class Facility(Base):
    __tablename__ = "facility_item"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    inst_code = Column(TEXT())
    tr_id = Column(TEXT())
    area = Column(TEXT())  # fix
    occupation = Column(TEXT())  # fix
    name = Column(TEXT())  # fix
    quantity = Column(TEXT())  # fix
    degree = Column(TEXT())
