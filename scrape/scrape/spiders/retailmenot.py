# -*- coding: utf-8 -*-

from scrape.items import RETAILMENOTItem
import datetime
import os
import re
import scrapy
import time


LOCAL_FILE_SCHEMA = 'file://'
ARCHIVE_PATH = '/home/gjoliver/archive/retailmenot/'


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
        offers = response.xpath('//div[contains(@class, "offer")]')
        for offer in offers:
            try:
                domain = offer.xpath('@data-storedomain').extract()[0]
                offerid = offer.xpath('@data-offerid').extract()[0]
                offertype = offer.xpath('@data-type').extract()[0]
                desc = offer.xpath(
                    './/h3[contains(@class, "title")]/a/text()').extract()[0]
                used_today = int(offer.xpath(
                    './/div[contains(@class, "info")]/text()').re(
                        r'(\d+) People Used Today')[0])

                item = RETAILMENOTItem(
                    uid=offerid,
                    site=domain,
                    offer_desc=desc,
                    offer_type=offertype,
                    used_today=used_today)

                yield item
            except (ValueError, IndexError):
                # Failed to extract something, give up.
                continue
