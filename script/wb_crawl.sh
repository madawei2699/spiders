#!/bin/bash

EPOCH=$(date +"%Y%m%d%H%M")

echo Start crawling. Epoch is $EPOCH.

# Crawl page.
while read LINE; do
    echo $LINE
    /usr/local/bin/phantomjs /home/gjoliver/spiders/phantom/wb.js $EPOCH $LINE
done < /home/gjoliver/urls/uid-list-wb

# Scrape data and store in CloudSql.
cd /home/gjoliver/spiders/scrape
/usr/bin/scrapy crawl WB -a epoch=$EPOCH -a db_host=$1 -a db_user=$2 -a db_passwd=$3
