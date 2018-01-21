import cookielib
import optparse
import os
import random
import time
import urllib2
import zlib

URL = 'https://www.instagram.com/web/search/topsearch/?context=blended&query=%%23%s'

REQUEST_HEADERS = [
    ('Accept', '*/*'),
    ('Accept-encoding', 'gzip, deflate, br'),
    ('Accept-language', 'en-US,zh-CN;q=0.8'),
    ('Referer', 'https://www.instagram.com/'),
    ('User-agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'),
    ('x-requested-with', 'XMLHttpRequest')
]


def fetch_one(tag, opener, out_file):
    print 'Fetching ... ', tag
    try:
        data = opener.open(URL % tag).read()
        json = zlib.decompress(data, 16 + zlib.MAX_WBITS)
        with open(out_file, 'w') as f:
            f.write(json)
    except Exception as e:
        print 'Failed to fetch ', tag, ': ', str(e)


def fetch(tag_list, cookie_file, out_dir):
    cookiejar = cookielib.LWPCookieJar()
    cookiejar.load(cookie_file)
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookiejar))

    opener.addheaders = REQUEST_HEADERS

    with open(tag_list, 'r') as f:
        for l in f.readlines():
            tag = l.strip()

            fetch_one(tag, opener, os.path.join(out_dir, tag))

            # Sleep anywhere between 60 to 90 seconds.
            time.sleep(60 + int(30 * random.random()))

    cookiejar.save(cookie_file)


if __name__ == '__main__':
    parser = optparse.OptionParser()

    parser.add_option("-l", "--tag_list", dest="tag_list", default='',
                      help='File containing the list of tags to fetch.')
    parser.add_option("-k", "--cookie_file", dest="cookie_file", default='',
                      help='File containing the login cookies.')
    parser.add_option("-o", "--out_dir", dest="out_dir", default='',
                      help='Directory to write the fetched data files..')

    (options, args) = parser.parse_args()

    assert options.tag_list != ''
    assert options.cookie_file != ''
    assert options.out_dir != ''

    fetch(options.tag_list, options.cookie_file, options.out_dir)
