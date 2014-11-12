# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Field, Item


class AuthorItem(Item):
    name = Field()
    bloglink = Field()


class PostItem(Item):
    content = Field()
    date = Field()
    category = Field()
    link = Field()
    title = Field()
    author_id = Field()
    urls = Field()
    urls_from_text = Field()
    comments = Field()
    tags = Field()
    urls = Field()

    def __str__(self):
        return self['link']
