from db_models import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship


def create_authors_table(engine):
    Base.metadata.create_all(engine)


class Authors(Base):
    __tablename__ = "authors"

    id = Column(Integer, primary_key=True)
    bloglink = Column("bloglink", String, unique=True)
    name = Column("name", String, unique=True)
    posts = relationship("Posts", order_by="Posts.id", backref="authors")
    comments = relationship("Comments", order_by="Comments.id", backref="authors")
