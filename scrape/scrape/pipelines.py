# -*- coding: utf-8 -*-

# Define your item pipelines here

import MySQLdb
import csv
import datetime
import os
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


class RETAILMENOTDBPipeline(object):
    def __init__(self):
        self.db = None
        self.should_apply = False

    def open_spider(self, spider):
        if spider.name != 'RETAILMENOT':
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

        print 'Saving deal:', item['offer_desc'], ', from: ', item['site']
        print 'Timestamp: ', spider.timestamp

        query = """
            INSERT INTO RETAILMENOT
            (UID, Timestamp, Site, OfferType, OfferDesc, UsedToday)
            VALUES
            ("%s", %d, "%s", "%s", "%s", %d);""" % (
                item['uid'], spider.timestamp, item['site'],
                item['offer_type'], item['offer_desc'], item['used_today'])

        cursor = self.db.cursor()
        cursor.execute(query)
        cursor.close()

        self.db.commit()

        return item


class SaveToCSVPipeline(object):
    def __init__(self):
        self.instructions = {
            'FB': ['uid', 'talking_about', 'visit', 'total_likes', 'new_likes'],
            'WB': ['uid', 'following', 'followers'],
            'NDUO': ['uid', 'downloads'],
            'RETAILMENOT': [
                'uid', 'site', 'offer_type', 'offer_desc', 'used_today'],
            'PIN': [
                'uid', 'boards', 'pins', 'followers', 'following', 'likes'],
            'INSTA': [
                'uid', 'posts', 'followers', 'following']
        }

    def process_item(self, item, spider):
        fields = self.instructions[spider.name]
        dt = datetime.datetime.utcfromtimestamp(spider.timestamp)
        outfile_name = '/home/j/data/%s/%s.csv' % (
            spider.name, dt.strftime('%Y%m%d-%H%M'))

        # Write column labels.
        if not os.path.isfile(outfile_name):
            with open(outfile_name, 'w') as outfile:
                writer = csv.writer(outfile, delimiter='|')
                writer.writerow(['date', 'time'] + fields)

        with open(outfile_name, 'a') as outfile:
            date = dt.strftime('%Y%m%d')
            time = dt.strftime('%H%M')
            values = [item[key] or '' for key in item.keys() if key != 'pics']

            writer = csv.writer(outfile, delimiter='|')
            writer.writerow([date, time] + values)

        if spider.name == 'INSTA':
            # Write the special instagram picture to crawl file.
            with open('/home/j/data/insta_pics_tmp', 'a') as outfile:
                for p in item['pics']:
                    if item['posts'] > 500 or item['followers'] < 100000:
                        continue

                    outfile.write(item['uid'] + '\t' + p + '\n')
