var system = require('system');
var args = system.args;

var fs = require('fs');

var uids = fs.read('/home/gjoliver/urls/uid-list-wb').split('\n');

var epoch = args[1];

var USER_AGENT =
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36';

var COOKIES = [
    {'name': 'SUB',
     'value': '_2AkMvlrmff8NhqwJRmP0RzWPjao12zgzEieKZykhEJRMxHRl-yT83qmsktRA9lWsJ-06slBmLcBd7MHXUW6g17A..',
     'domain': '.weibo.com'},
    {'name': 'SUBP',
     'value': '0033WrSXqPxfM72-Ws9jqgMF55529P9D9WFqzykw_0_4JkXLpbHu3ka8',
     'domain': '.weibo.com'},
    {'name': 'SINAGLOBAL',
     'value': '3919988986493.206.1485582174688',
     'domain': '.weibo.com'},
    {'name': '_s_tentry',
     'value': 'baike.baidu.com',
     'domain': '.weibo.com'},
    {'name': 'Apache',
     'value': '3919988986493.206.1485582174688',
     'domain': '.weibo.com'},
    {'name': 'ULV',
     'value': '1485582174704:1:1:1:3919988986493.206.1485582174688:',
     'domain': '.weibo.com'},
    {'name': 'UOR',
     'value': 'ent.qianzhan.com,widget.weibo.com,www.7y7.com',
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
    page.settings.loadImages = false;
    page.settings.resourceTimeout = 5000;
    page.customHeaders = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*',
        'Accept-Language': 'en-US,en',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
	'Referer': 'http:www.baidu.com/'
    };

    var url = 'http:weibo.com/' + uid;
    page.open(url, function (status) {
        if (status === 'fail') {
            console.log('Failed to fetch page: ' + url);
            next.apply();
            return;
        }

        window.setTimeout(function () {
	    console.log(Date().toString() + ': Saving page: ' + url);

	    fs.write('/archd/archive/wb/' +
		     epoch + '/' + uid.replace('/', '-').toLowerCase(),
		     page.content,
		     'w');
	    page.close();

            next.apply();
            // Wait randomly between 60 to 120 seconds for the page to
            // actually render.
            // This delay also serves as a protection so we are not easily
            // detected as a scraper.
        }, 60000 + (60000 * Math.random()));
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
