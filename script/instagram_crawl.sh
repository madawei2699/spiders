#!/bin/bash

EPOCH=$(date +"%Y%m%d%H%M")

echo Start crawling. Epoch is $EPOCH.

rm -f /home/j/data/insta_pics_tmp

# Crawl page.
while read LINE; do
    echo $LINE
    /usr/local/bin/phantomjs /home/gjoliver/spiders/phantom/instagram.js $EPOCH $LINE
done < /home/gjoliver/urls/uid-list-instagram

# Scrape data and store in CloudSql.
cd /home/gjoliver/spiders/scrape
/usr/bin/scrapy crawl INSTA -a epoch=$EPOCH -a db_host=$1 -a db_user=$2 -a db_passwd=$3

if [ -f /home/j/data/insta_pics_tmp ]; then
    mv /home/j/data/insta_pics_tmp /home/j/data/insta_pics
fi
