# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class GzInformationItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    cnt = scrapy.Field()
    sub_url = scrapy.Field()
    pass
