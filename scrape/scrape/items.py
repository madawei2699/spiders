# -*- coding: utf-8 -*-

# Define here the models for your scraped items

import scrapy


class FBItem(scrapy.Item):
    uid = scrapy.Field()
    talking_about = scrapy.Field()
    visit = scrapy.Field()
    total_likes = scrapy.Field()
    new_likes = scrapy.Field()


class WBItem(scrapy.Item):
    uid = scrapy.Field()
    following = scrapy.Field()
    followers = scrapy.Field()


class NDUOItem(scrapy.Item):
    uid = scrapy.Field()
    downloads = scrapy.Field()

class RETAILMENOTItem(scrapy.Item):
    uid = scrapy.Field()
    site = scrapy.Field()
    offer_type = scrapy.Field()
    offer_desc = scrapy.Field()
    used_today = scrapy.Field()
