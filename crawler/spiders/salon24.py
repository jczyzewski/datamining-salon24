# -*- coding: utf-8 -*-
import re
from datetime import datetime

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.selector import Selector

from crawler.items import AuthorItem, PostItem


class Salon24Spider(CrawlSpider):
    name = "salon24"
    allowed_domains = ["salon24.pl"]
    # start from the first page of blog catalog
    start_urls = (
        'http://www.salon24.pl/katalog-blogow/0,1,Nick,1',
    )
    rules = (
        # follow catalog pages
        Rule(LinkExtractor(allow=('http://www.salon24.pl/catalog/0,\d,Nick,1', ), )),

        # Extract blog's links and parse them
        Rule(LinkExtractor(allow=('\S+\.salon24\.pl/$', )),
             callback='parse_blog_link', follow=True),

        # blog subpages
        Rule(LinkExtractor(allow='\S+\.salon24\.pl/posts/0,\d+,wszystkie')),
        # post page
        # example: http://rybitzky.salon24.pl/posts/0,2,wszystkie
        Rule(LinkExtractor(allow=('\S+\.salon24\.pl/\d+,\S+', ), restrict_xpaths="//ul[@class='post-list']"),
             callback='parse_post_page', follow=False),
    )


    def parse_blog_link(self, response):
        autor = AuthorItem()
        autor['bloglink'] = response.url
        autor['name'] = re.sub('[{}"]', '', response.xpath("//div[@class='author-about-body']/h2/text()").extract()[0])
        return autor

    def parse_post_page(self, response):
        # http://gelberg.salon24.pl/610273,co-sie-stalo-z-nagroda-ksiedza-jerzego

        post = PostItem()
        date = response.xpath(
            "//div[@class='content-left']/article[@class='post']/header/span[1]/text()").extract()
        post['date'] = self.parse_date(date[0])
        post['category'] = response.xpath(
            "//div[@class='content-left']/article[@class='post']/header/span[2]/text()").extract()
        post['link'] = response.url
        post['title'] = response.xpath(
            "//div[@class='content-left']/article[@class='post']/header/h1/text()").extract()
        post['author_id'] = response.xpath("//div[@class='author-about-body']/a/text()").extract()
        post['content'] = response.xpath(
            "//div[@class='bbtext']//text()").extract()
        post['urls'] = response.xpath(
            "//div[@class='bbtext']//a/@href").extract()
        post['tags'] = response.xpath("//div[@class='post-tags']/a//text()").extract()
        selector = Selector(response)
        comments = []
        for li in selector.xpath("////*[@id='komentarze']/ul/li"):
            date = li.xpath("div[@class='author-box']/div/span/text()").extract()
            cmnt = {'title': ''.join(li.xpath("h3/text()").extract()).strip(),
                    'content': ''.join([s.encode('utf-8') for s in
                                        li.xpath("div[@class='comment-body'][1]//text()").extract()]).strip(),
                    'author_id': li.xpath("div[@class='author-box']/div/a/text()").extract(),
                    'author_bloglink': li.xpath("div[@class='author-box']/div/a/@href").extract(),
                    'urls': ';'.join([s.encode('utf-8') for s in
                                      li.xpath("div[@class='comment-body'][1]//a/@href").extract()]).strip(),
                    'date': self.parse_date(date[0]) if date else None}
            comments.append(cmnt)
        post['comments'] = comments
        return post


    def parse_date(self, date):
        """
        Dates at salon24 come at three different formats
        :param date:
        """
        full_date_format = "%d.%m.%Y %H:%M"
        current_year_date_format = "%d.%m %H:%M"
        current_day_date_format = "%H:%M"
        try:
            parsed = datetime.strptime(date, full_date_format);
        except ValueError:
            try:
                today = datetime.now()
                parsed = datetime.strptime(date, current_year_date_format)
                parsed = parsed.replace(year=today.year)
            except ValueError:
                parsed = datetime.strptime(date, current_day_date_format)
                parsed = parsed.replace(year=today.year, month=today.month, day=today.day)
        return parsed
