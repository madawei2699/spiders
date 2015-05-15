'''Sample command line:
  python fetch_trend.py --t=Walmart
                        --u=user_name
                        --p=pass_word
                        --outfile=/tmp/report.csv
'''

import argparse
import gtrends 
import time
from random import randint
import urllib2

def DownloadCSV2(tickers, username, password, outfile):
    connector = gtrends.GTrends(username, password)
    connector.request_report(','.join(tickers))

    #wait a random amount of time between requests to avoid bot detection
    time.sleep(randint(5, 10))

    connector.save_csv(outfile)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='fetch_trends.')
    parser.add_argument('-t', '--tickers', type=str, help='One ticker to study.',
                        default=[], action='append')
    parser.add_argument('-u', '--username', type=str, help='Google username.',
                        default='', action='store')
    parser.add_argument('-p', '--password', type=str, help='Google password.',
                        default='', action='store')
    parser.add_argument('-o', '--outfile', type=str, help='Output CSV file.',
                        default='', action='store')
    args = parser.parse_args()

    DownloadCSV2(args.tickers, args.username, args.password, args.outfile)
