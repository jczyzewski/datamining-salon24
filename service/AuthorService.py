from sqlalchemy import func
from models.authors import Authors


class AuthorService:
    def __init__(self, session):
        self.Session = session

    def get_author_by_name(self, author_name):
        return self.Session.query(Authors).filter(func.lower(Authors.name) == func.lower(author_name)).first()
