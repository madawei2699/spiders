#!/bin/bash

EPOCH=$(date +"%Y%m%d%H%M")

echo Start crawling. Epoch is $EPOCH.

mkdir -p /archd/archive/instagram_tag/$EPOCH

# Crawl page.
python /home/gjoliver/spiders/phantom/instagram_tag.py -l /home/gjoliver/urls/uid-list-instagram -k /home/gjoliver/insta_cookies_lwp -o /archd/archive/instagram_tag/$EPOCH

# Scrape data and store in CloudSql.
python /home/gjoliver/spiders/scrape/scrape/spiders/instagram_tag.py -i /archd/archive/instagram_tag/$EPOCH -o /home/j/data/INSTA_TAG/$EPOCH.csv
