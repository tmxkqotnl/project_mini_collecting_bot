import uuid
from sqlalchemy import TEXT, Column
from src.db.db import Base
from sqlalchemy.dialects.postgresql import UUID

# fix - type fix
class Equipment(Base):
    __tablename__ = 'equipment_item'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    inst_code = Column(TEXT())
    tr_id = Column(TEXT())
    name = Column(TEXT())  # fix
    quantity = Column(TEXT())  # fix
