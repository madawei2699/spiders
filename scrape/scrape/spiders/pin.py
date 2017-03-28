# -*- coding: utf-8 -*-

from scrape.items import PINItem
import datetime
import os
import re
import scrapy
import time


LOCAL_FILE_SCHEMA = 'file://'
ARCHIVE_PATH = '/archd/archive/pinterest/'


def extractValue(response, name):
    try:
        text = response.xpath(
            '//meta[contains(@name, "' + name + '")]/@content').extract()[0]
        if text:
            return int(text.strip().replace(',', ''))
        else:
            return 0
    except (ValueError, IndexError):
        return 0


class PINPageSpider(scrapy.Spider):
    name = 'PIN'
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
        item = PINItem(
            uid=response.url.split('/')[-1],
            boards=extractValue(response, 'pinterestapp:boards'),
            followers=extractValue(response, 'pinterestapp:follower'),
            following=extractValue(response, 'pinterestapp:following'))
        yield item
