# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class JournalFigure(scrapy.Item):
    title = scrapy.Field()
    auth_list = scrapy.Field()
    journal = scrapy.Field()
    pubDate = scrapy.Field()
    doi = scrapy.Field()
    figTitle = scrapy.Field()
    figCaption = scrapy.Field()
    file_urls = scrapy.Field()
    files = scrapy.Field()
