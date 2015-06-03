# -*- coding: utf-8 -*-

from scrape.items import RETAILMENOTItem
import datetime
import os
import re
import scrapy
import time


LOCAL_FILE_SCHEMA = 'file://'
ARCHIVE_PATH = '/home/gjoliver/archive/retailmenot/'


def extractDownloads(response):
    try:
        text = response.xpath('//span[@class="count"]/text()').extract()[0]
        match = re.search('^\d+', text.replace(',', ''))
        if match:
            return int(match.group(0))
        else:
            return 0
    except (ValueError, IndexError):
        return 0


class RETAILMENOTPageSpider(scrapy.Spider):
    name = 'RETAILMENOT'
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
        site = response.url.split('/')[-1]

        offers = response.xpath('//div[contains(@class, "offer")]')
        for offer in offers:
            try:
                desc = offer.xpath(
                    './/contains(@class, "title")/a/text()]').extract()[0]

                item = RETAILMENOTItem(
                    site=site,
                    offer_desc=desc)

                yield item
            except IndexError:
                # Failed to extract something, give up.
                continue
