from models.tags import Tags

__author__ = 'kuba cz'

class TagsService:
    def __init__(self, session):
        self.Session = session

    def get_tag_by_name(self, tag):
        return self.Session.query(Tags).filter_by(name=tag).first()