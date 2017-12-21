#!/bin/bash

EPOCH=$(date +"%Y%m%d%H%M")
LIST_NAME=insta_pics_$EPOCH

echo Start crawling. Epoch is $LIST_NAME.

cp /home/j/data/insta_pics /home/j/data/$LIST_NAME

# Crawl page.
while read LINE; do
    set $LINE
    echo $1 $2
    /usr/local/bin/phantomjs /home/gjoliver/spiders/phantom/instagram_pics.js $EPOCH $1 $2
done < /home/j/data/$LIST_NAME

if [ -f /home/j/data/$LIST_NAME ]; then
    rm /home/j/data/$LIST_NAME
fi

# Scrape data and store in CloudSql.
cd /home/gjoliver/spiders/scrape
/usr/bin/scrapy crawl INSTA_PICS -a epoch=$EPOCH -a db_host=$1 -a db_user=$2 -a db_passwd=$3
