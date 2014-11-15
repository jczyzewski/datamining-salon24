from sqlalchemy import Column, Integer, String

from db_models import Base


class Tags(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True)
    name = Column("name", String, unique=True, nullable=False)

    def __init__(self, tag):
        self.name = tag
