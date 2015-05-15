# -*- coding: utf-8 -*-

# Define your item pipelines here

import MySQLdb
import scrapy


class FBDBPipeline(object):
    def __init__(self):
        self.db = None

    def open_spider(self, spider):
        self.db = MySQLdb.connect(host=spider.db_host,
                                  db='data',
                                  user=spider.db_user,
                                  passwd=spider.db_passwd,
                                  charset='utf8')
        scrapy.log.msg('DB connected.', scrapy.log.INFO)

    def close_spider(self, spider):
        # Just in case there is anything un-committed.
        self.db.commit()
        self.db.close()

    def process_item(self, item, spider):
        print 'Saving item UID: ', item['uid']
        print 'Timestamp: ', spider.timestamp

        query = """
            INSERT INTO FB
            (UID, Timestamp, TalkingAbout, Visit, TotalLikes, NewLikes)
            VALUES
            ("%s", %d, %d, %d, %d, %d);""" % (
                item['uid'], spider.timestamp, item['talking_about'],
                item['visit'], item['total_likes'], item['new_likes'])

        cursor = self.db.cursor()
        cursor.execute(query)
        cursor.close()

        self.db.commit()

        return item
