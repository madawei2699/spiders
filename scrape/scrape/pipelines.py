# -*- coding: utf-8 -*-

# Define your item pipelines here

import MySQLdb
import scrapy


class FBDBPipeline(object):
    def __init__(self):
        self.db = None
        self.should_apply = False

    def open_spider(self, spider):
        if spider.name != 'FB':
            return

        self.should_apply = True
        self.db = MySQLdb.connect(host=spider.db_host,
                                  db='data',
                                  user=spider.db_user,
                                  passwd=spider.db_passwd,
                                  charset='utf8')
        scrapy.log.msg('DB connected.', scrapy.log.INFO)

    def close_spider(self, spider):
        if not self.should_apply or not self.db:
            return

        # Just in case there is anything un-committed.
        self.db.commit()
        self.db.close()

    def process_item(self, item, spider):
        if not self.should_apply or not self.db:
            return item

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


class WBDBPipeline(object):
    def __init__(self):
        self.db = None
        self.should_apply = False

    def open_spider(self, spider):
        if spider.name != 'WB':
            return

        self.should_apply = True
        self.db = MySQLdb.connect(host=spider.db_host,
                                  db='data',
                                  user=spider.db_user,
                                  passwd=spider.db_passwd,
                                  charset='utf8')
        scrapy.log.msg('DB connected.', scrapy.log.INFO)

    def close_spider(self, spider):
        if not self.should_apply or not self.db:
            return

        # Just in case there is anything un-committed.
        self.db.commit()
        self.db.close()

    def process_item(self, item, spider):
        if not self.should_apply or not self.db:
            return item

        print 'Saving item UID: ', item['uid']
        print 'Timestamp: ', spider.timestamp

        query = """
            INSERT INTO WB
            (UID, Timestamp, Following, Followers)
            VALUES
            ("%s", %d, %d, %d);""" % (
                item['uid'], spider.timestamp,
                item['following'], item['followers'])

        cursor = self.db.cursor()
        cursor.execute(query)
        cursor.close()

        self.db.commit()

        return item


class NDUODBPipeline(object):
    def __init__(self):
        self.db = None
        self.should_apply = False

    def open_spider(self, spider):
        if spider.name != 'NDUO':
            return

        self.should_apply = True
        self.db = MySQLdb.connect(host=spider.db_host,
                                  db='data',
                                  user=spider.db_user,
                                  passwd=spider.db_passwd,
                                  charset='utf8')
        scrapy.log.msg('DB connected.', scrapy.log.INFO)

    def close_spider(self, spider):
        if not self.should_apply or not self.db:
            return

        # Just in case there is anything un-committed.
        self.db.commit()
        self.db.close()

    def process_item(self, item, spider):
        if not self.should_apply or not self.db:
            return item

        print 'Saving item UID: ', item['uid']
        print 'Timestamp: ', spider.timestamp

        query = """
            INSERT INTO NDUO
            (UID, Timestamp, Downloads)
            VALUES
            ("%s", %d, %d);""" % (
                item['uid'], spider.timestamp, item['downloads'])

        cursor = self.db.cursor()
        cursor.execute(query)
        cursor.close()

        self.db.commit()

        return item
