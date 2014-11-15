# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import re
from sqlalchemy.orm import sessionmaker

from crawler.items import PostItem, AuthorItem
from models.authors import Authors
from models.comments import Comments
from models.db_models import db_connect
from models.posts import Posts, create_posts_table
from models.tags import Tags

from service.AuthorService import AuthorService
from service.TagsService import TagsService


class DbPipeline(object):
    def __init__(self):
        engine = db_connect()
        create_posts_table(engine)
        self.Session = sessionmaker(bind=engine)
        self.session = self.Session()
        self.AuthorService = AuthorService(session=self.session)
        self.TagsService = TagsService(session=self.session)

    def process_item(self, item, spider):
        if isinstance(item, PostItem):
            db_item = Posts()
            author = self.AuthorService.get_author_by_name(item['author_id'][0])
            db_item.author_id = author.id
            db_item.category = ''.join(item['category']).strip().replace("Kategoria: ", '')
            db_item.content = ''.join(item['content']).strip().replace('/n', '')
            db_item.date = item['date']
            db_item.link = item['link']
            db_item.title = ''.join(item['title']).strip()
            db_item.comments = self.process_comments(item['comments'])
            db_item.tags = self.process_tags(item['tags'])
            urls = ";".join([url for url in item['urls'] if "salon24.pl" in url]).strip()
            db_item.urls = urls if urls and urls is not "''" else None
        if isinstance(item, AuthorItem):
            db_item = Authors(**item)
            db_item.name = ''.join(db_item.name).strip().replace('"', '').upper()

        try:
            self.session.add(db_item)
            self.session.commit()
        except:
            self.session.rollback()
            raise
        finally:
            self.session.close()

        return item

    def process_comments(self, comments):
        cmnts_list = []
        for c in comments:

            new_comment = Comments(**c)
            salon_urls_regex = re.compile("\S+\.salon24\.pl\S*")
            urls = ";".join(salon_urls_regex.findall(new_comment.content)).strip()
            new_comment.urls = urls if urls and urls is not "''" else None
            if not c['author_id']:
                continue

            author = self.AuthorService.get_author_by_name(c['author_id'][0])
            if author is None:
                new_author = Authors()
                name = c['author_id']
                new_author.name = ''.join(name).strip().replace('"', '').upper()
                new_author.bloglink = ''.join(c['author_bloglink']).replace('"', '')
                session = self.session
                try:
                    session.add(new_author)
                    session.commit()
                except:
                    session.rollback()
                    raise
                new_comment.author_id = new_author.id
            else:
                new_comment.author_id = author.id
            if new_comment.title.startswith('@'):
                self.match_parent_comment(cmnts_list, new_comment)

            cmnts_list.append(new_comment)
            self.session.add(new_comment)
            self.session.flush()
            self.session.refresh(new_comment)
        return cmnts_list

    def process_tags(self, tags):
        tags_list = []
        for t in tags:
            tag = self.TagsService.get_tag_by_name(tag=t)
            tag = tag if tag is not None else Tags(t)
            tags_list.append(tag)
        return tags_list

    def match_parent_comment(self, cmnts_list, new_comment):
        ref_comment_author = new_comment.title.replace('@', '')
        ref_comment_author_id = self.AuthorService.get_author_by_name(ref_comment_author)
        if ref_comment_author_id is not None:
            for cm in reversed(cmnts_list):
                if cm.author_id == ref_comment_author_id.id:
                    new_comment.parent_comment = cm.id