import uuid
from sqlalchemy import TEXT, Column
from src.db.db import Base
from sqlalchemy.dialects.postgresql import UUID


class Article(Base):
    __tablename__ = "article"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    writer = Column(UUID())
    content = Column(TEXT())
    file_path = Column(TEXT())
    