# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class UniversityWebPageItem(scrapy.Item):
    url = scrapy.Field()
    score = scrapy.Field()

class LecturerPageItem(scrapy.Item):
    url = scrapy.Field()
    subject = scrapy.Field()
