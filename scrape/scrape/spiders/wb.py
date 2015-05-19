# -*- coding: utf-8 -*-

from scrape.items import WBItem
import datetime
import os
import scrapy
import time


LOCAL_FILE_SCHEMA = 'file://'
ARCHIVE_PATH = '/home/gjoliver/archive/wb/'


def extractBrother(response, text):
    try:
        return int(response.xpath(
            '//span[text()="%s"]/preceding-sibling::*/text()' % text)
            .extract()[0].replace(',', ''));
    except (ValueError, IndexError):
        return 0


class WBPageSpider(scrapy.Spider):
    name = 'WB'
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
        item = WBItem(
            uid=response.url.split('/')[-1],
            following=extractBrother(response, '关注'),
            followers=extractBrother(response, '粉丝'))
        yield item
