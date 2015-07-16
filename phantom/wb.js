var system = require('system');
var args = system.args;

var fs = require('fs');

var uids = fs.read('/home/gjoliver/urls/uid-list-wb').split('\n');

var epoch = args[1];

var USER_AGENT =
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 ' +
    '(KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36 ' +
    'OPR/29.0.1795.47';


var COOKIES = [
    {'name': 'SUB',
     'value': '_2AkMiBKVhf8NjqwJRmPoUym3ibItyyQnEiebDAHzsJxJTHnNI7M4LFY9GFWT_OLz_MhI166vDiRRl',
     'domain': '.weibo.com'},
    {'name': 'SUBP',
     'value': '0033WrSXqPxfM72-Ws9jqgMF55z29P9D9Wh1aZycWgz3jVFOCbIPvEjv',
     'domain': '.weibo.com'},
    {'name': 'SINAGLOBAL',
     'value': '4578747055493.295.1431844878252',
     'domain': '.weibo.com'},
    {'name': 'YF-Page-G0',
     'value': '046bedba5b296357210631460a5bf1d2',
     'domain': '.weibo.com'},
    {'name': '_s_tentry',
     'value': '-',
     'domain': '.weibo.com'},
    {'name': 'Apache',
     'value': '5785534891765.564.1432019043639',
     'domain': '.weibo.com'},
    {'name': 'ULV',
     'value': '1432019043861:3:3:2:5785534891765.564.1432019043639:1431928606311',
     'domain': '.weibo.com'},
    {'name': 'YF-Ugrow-G0',
     'value': 'ea90f703b7694b74b62d38420b5273df',
     'domain': '.weibo.com'}
];
for (var i = 0; i < COOKIES.length; i++) {
    phantom.addCookie(COOKIES[i]);
}


var processUid = function(uid, next) {
    if (uid.replace(/ /g, '') == '') {
        next.apply();
        return;
    }

    var page = require('webpage').create();
    page.settings.userAgent = USER_AGENT;
    page.customHeaders = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*',
        'Accept-Language': 'en-US,en',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive'
    };

    var url = 'http://weibo.com/' + uid;
    page.open(url, function (status) {
        if (status === 'fail') {
            console.log('Failed to fetch page: ' + url);
            next.apply();
            return;
        }

        window.setTimeout(function () {
            console.log('Saving page: ' + url);

            fs.write('/home/gjoliver/archive/wb/' +
                     epoch + '/' + uid.replace('/', '-').toLowerCase(),
                     page.content,
                     'w');
            page.close();

            next.apply();
        // Wait randomly between 3 to 10 seconds for the page to
        // actually render.
        // This delay also serves as a protection so we are not easily
        // detected as a scraper.
        }, 3000 + (12000 * Math.random()));
    });
}

var crawlNext = function() {
    if (uids.length > 0) {
        var uid = uids[0];
        uids.splice(0, 1);
        processUid(uid, crawlNext);
    } else {
        phantom.exit();
    }
}

crawlNext();
