# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

"""
Definition of a news item

Contains all data fields that scrapy will try to fill for each article we scrape.
"""
class CnnItem(scrapy.Item):
    date = scrapy.Field()
    title = scrapy.Field()
    url = scrapy.Field()
    author = scrapy.Field()
    textshort = scrapy.Field()
    textfull = scrapy.Field()
