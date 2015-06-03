# -*- coding: utf-8 -*-

# Scrapy settings for crawl project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'xiaobai'

SPIDER_MODULES = ['scrape.spiders']
NEWSPIDER_MODULE = 'scrape.spiders'
ITEM_PIPELINES = {'scrape.pipelines.FBDBPipeline': 100,
                  'scrape.pipelines.WBDBPipeline': 200,
                  'scrape.pipelines.NDUODBPipeline': 300,
                  'scrape.pipelines.RETAILMENOTDBPipeline': 400}

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'crawl (+http://www.yourdomain.com)'
