from db_models import Base
from sqlalchemy import Column, Integer, String, Text, Date, ForeignKey, TIMESTAMP, Table
from sqlalchemy.orm import relationship


def create_posts_table(engine):
    Base.metadata.create_all(engine)


post_tags = Table('post_tags', Base.metadata,
                      Column('post_id', Integer, ForeignKey('posts.id')),
                      Column('tag_id', Integer, ForeignKey('tags.id')))


class Posts(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True)
    category = Column("category", String)
    content = Column("content", Text)
    date = Column("date", TIMESTAMP)
    link = Column("link", String)
    title = Column("title", String)
    author_id = Column("author_id", Integer, ForeignKey('authors.id'))
    urls = Column("urls",String)
    comments = relationship("Comments", order_by="Comments.id", backref="post")
    tags = relationship('Tags', secondary=post_tags, backref='posts')


