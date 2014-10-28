# -*- coding: utf-8 -*-
import scrapy
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.selector import HtmlXPathSelector
from crawler.items import AuthorItem, PostItem


class Salon24Spider(CrawlSpider):
    name = "salon24"
    allowed_domains = ["salon24.pl"]
    # start from the first page of blog catalog
    start_urls = (

        'http://rafalziemkiewicz.salon24.pl/472393,podroz-koleja-skraca-czas-podrozy-pociagiem',
    )
    rules = (
        # follow catalog pages
        #Rule(LinkExtractor(allow=('http://www.salon24.pl/catalog/0,\d,Nick,1', ), )),

        # Extract blog's links and parse them
        #Rule(LinkExtractor(allow=('\S+\.salon24\.pl/$', )), callback='parse_blog_link', follow=True),

        #Blog main page
        Rule(LinkExtractor(allow=('\S+\.salon24\.pl/\d+,\S+', ),), callback='parse_post_page', follow=False),
    )


    def parse_blog_link(self, response):
        autor = AuthorItem()
        autor['bloglink'] = response.url
        autor['name'] = response.xpath("//div[@class='author-about-body']/h2/text()").extract()
        return autor

    def parse_post_page(self, response):
        #http://gelberg.salon24.pl/610273,co-sie-stalo-z-nagroda-ksiedza-jerzego

        print "POST POST POST POST POST POST POST"
        post = PostItem()
        post['date'] = response.xpath(
            "//div[@class='content-left']/article[@class='post']/header/span[1]/text()").extract()
        post['category'] = response.xpath(
            "//div[@class='content-left']/article[@class='post']/header/span[2]/text()").extract()
        post['link'] = response.url
        post['title'] = response.xpath(
            "//div[@class='content-left']/article[@class='post']/header/h1/text()").extract()
        post['author'] = response.xpath("//div[@class='author-about-body']/a/text()").extract()
        post['content'] = response.xpath(
            "//div[@class='bbtext']//text()").extract()
        post['tags'] = response.xpath("//div[@class='post-tags']/a//text()").extract()
        selector = HtmlXPathSelector(response)
        comments = []
        for li in selector.select("////*[@id='komentarze']/ul/li"):
            cmnt = {'title': li.xpath("h3/text()").extract(),
                    'content': [s.encode('utf-8') for s in li.xpath("div[@class='comment-body'][1]/text()").extract()],
                    'author': li.xpath("div[@class='author-box']/div/a/text()").extract(),
                    'date': li.xpath("div[@class='author-box']/div/span/text()").extract()}
            comments.append(cmnt)
        post['comments'] = comments
        return post
