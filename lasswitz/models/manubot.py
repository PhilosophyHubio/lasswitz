from sqlalchemy import (
    Column,
    Index,
    Integer,
    Text,
    DateTime,
    Uuid
)

from .meta import Base


class Manuscript(Base):
    __tablename__ = 'manuscript'
    id = Column(Uuid, primary_key=True)
    title = Column(Text)
    abstract = Column(Text)
    body = Column(Text)
    revision = Column(Integer)
    tag = Column(Text)
    keywords = Column(Text)
    date = Column(DateTime)
    language = Column(Text)
