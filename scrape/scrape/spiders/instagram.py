# -*- coding: utf-8 -*-

from scrape.items import INSTAItem
import datetime
import os
import re
import scrapy
import time


LOCAL_FILE_SCHEMA = 'file://'
ARCHIVE_PATH = '/archd/archive/instagram/'


def extractValue(response, class_name):
    try:
        try:
            text = response.xpath(
                '//span[contains(@class, "' + class_name + '")]/@title').extract()[0]
        except IndexError:
            # Try raw text.
            text = response.xpath(
                '//span[contains(@class, "' + class_name + '")]/text()').extract()[0]

        if text:
            if text[-1] == 'k':
                return int(float(text[:-1].strip().replace(',', '')) * 1000)
            else:
                return int(float(text.strip().replace(',', '')))
        else:
            return 0
    except (ValueError, IndexError):
        return 0


class INSTAPageSpider(scrapy.Spider):
    name = 'INSTA'
    allowed_domains = []
    # To be populated in constructor.
    start_urls = None

    def __init__(self, epoch=None, db_host=None, db_user=None, db_passwd=None):
        assert epoch
        assert db_host
        assert db_user
        assert db_passwd

        self.db_host = db_host
        self.db_user = db_user
        self.db_passwd = db_passwd

        self.timestamp = time.mktime(
            datetime.datetime.strptime(epoch, '%Y%m%d%H%M').timetuple())
        self.log('Crawling page from epoch timestamp: %d' % self.timestamp,
                 level=scrapy.log.INFO)

        # Find all the data files to scrape from.
        self.start_urls = [(LOCAL_FILE_SCHEMA + ARCHIVE_PATH + epoch + '/' + f)
                           for f in os.listdir(ARCHIVE_PATH + epoch)]

    def parse(self, response):
        item = INSTAItem(
            uid=response.url.split('/')[-1],
            posts=extractValue(response, 'PostsStatistic'),
            followers=extractValue(response, 'FollowedByStatistic'),
            following=extractValue(response, 'FollowsStatistic'))
        yield item
