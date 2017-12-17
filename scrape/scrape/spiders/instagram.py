# -*- coding: utf-8 -*-

from scrape.items import INSTAItem
import datetime
import os
import re
import scrapy
import time


LOCAL_FILE_SCHEMA = 'file://'
ARCHIVE_PATH = '/archd/archive/instagram/'


def extractPictures(response):
    regexp = '//a[starts-with(@href, "/p/")]/@href'
    try:
        pics = response.xpath(regexp).extract()
    except (ValueError, IndexError):
        return []

    cleaned_pics = []
    for p in pics:
        idx = p.find('?')
        if idx > 0:
            cleaned_pics.append(p[:idx])
        elif len(p) > 0:
            cleaned_pics.append(p)

    return cleaned_pics


def extractBrotherText(response, text):
    regexp = '//span[contains(text(), "%s")]/span[1]/text()' % text
    try:
        text = response.xpath(regexp).extract()[0].replace(',', '')
    except (ValueError, IndexError):
        return 0

    if text:
        if text[-1] == 'm':
            return int(float(text[:-1].strip().replace(',', '')) * 1000000)
        elif text[-1] == 'k':
            return int(float(text[:-1].strip().replace(',', '')) * 1000)
        else:
            return int(float(text.strip().replace(',', '')))
    else:
        return 0


def extractBrotherTitle(response, text):
    regexp = '//span[contains(text(), "%s")]/span[1]/@title' % text
    try:
        text = response.xpath(regexp).extract()[0].replace(',', '')
    except (ValueError, IndexError):
        return 0

    if text:
        if text[-1] == 'm':
            return int(float(text[:-1].strip().replace(',', '')) * 1000000)
        elif text[-1] == 'k':
            return int(float(text[:-1].strip().replace(',', '')) * 1000)
        else:
            return int(float(text.strip().replace(',', '')))
    else:
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
            posts=extractBrotherText(response, ' posts'),
            followers=extractBrotherTitle(response, ' followers'),
            following=extractBrotherText(response, ' following'),
            pics=extractPictures(response))
        print item
        yield item
