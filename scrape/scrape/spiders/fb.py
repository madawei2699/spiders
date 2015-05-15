from scrape.items import FBItem
import datetime
import os
import scrapy
import time


LOCAL_FILE_SCHEMA = 'file://'
ARCHIVE_PATH = '/home/gjoliver/archive/fb/'


def extractBrother(response, text):
    try:
        return int(response.xpath(
            '//div[text()="%s"]/preceding-sibling::*/text()' % text)
            .extract()[0].replace(',', ''));
    except (ValueError, IndexError):
        return 0


class FBPageSpider(scrapy.Spider):
    name = 'FB'
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
        item = FBItem(
            uid=response.url.split('/')[-1],
            talking_about=extractBrother(response, 'People Talking About This'),
            visit=extractBrother(response, 'People Checked In Here'),
            total_likes=extractBrother(response, 'Total Page Likes'),
            new_likes=extractBrother(response, 'New Page Likes'))
        yield item
