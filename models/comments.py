from db_models import Base
from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, ForeignKey


class Comments(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True)
    parent_comment = Column("parent_comment", Integer)
    content = Column("content", Text)
    date = Column("date", TIMESTAMP)
    title = Column("title", String)
    author_id = Column("author_id", Integer, ForeignKey('authors.id'))
    post_id = Column("post_id", Integer, ForeignKey('posts.id'))
    urls = Column("urls",String)
    author_bloglink = ""
