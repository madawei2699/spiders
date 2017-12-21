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
    posts = scrapy.Field()


class NDUOItem(scrapy.Item):
    uid = scrapy.Field()
    downloads = scrapy.Field()


class RETAILMENOTItem(scrapy.Item):
    uid = scrapy.Field()
    site = scrapy.Field()
    offer_type = scrapy.Field()
    offer_desc = scrapy.Field()
    used_today = scrapy.Field()


class PINItem(scrapy.Item):
    uid = scrapy.Field()
    boards = scrapy.Field()
    pins = scrapy.Field()
    followers = scrapy.Field()
    following = scrapy.Field()
    likes = scrapy.Field()


class INSTAItem(scrapy.Item):
    uid = scrapy.Field()
    posts = scrapy.Field()
    followers = scrapy.Field()
    following = scrapy.Field()
    pics = scrapy.Field()

class INSTAPicItem(scrapy.Item):
    acct = scrapy.Field()
    uid = scrapy.Field()
    likes = scrapy.Field()
    views = scrapy.Field()
