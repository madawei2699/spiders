var system = require('system');
var args = system.args;

var fs = require('fs');

var urls = fs.read('/home/gjoliver/urls/retailmenot-url').split('\n');

var epoch = args[1];

var USER_AGENT =
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 ' +
    '(KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36 ' +
    'OPR/29.0.1795.47';

var processUrl = function(url, next) {
    if (url.replace(/ /g, '') == '') {
        next.apply();
        return;
    }

    var page = require('webpage').create();
    page.settings.userAgent = USER_AGENT;
    page.open('http://www.retailmenot.com/view/' + url, function (status) {
        if (status === 'fail') {
            console.log('Failed to fetch page: ' + url);
            next.apply();
            return;
        }

        window.setTimeout(function () {
            console.log('Saving page: ' + url);

            var uid = url;
            fs.write('/archd/archive/retailmenot/' +
                     epoch + '/' + uid.toLowerCase(),
                     page.content,
                     'w');
            page.close();

            next.apply();
        // Wait randomly between 1 to 3 mins for the page to
        // actually render.
        // Use especially longer timeout since retailmenot seems to have
        // pretty rigorous detection on bots.
        // This delay also serves as a protection so we are not easily
        // detected as a scraper.
        }, 60000 + (120000 * Math.random()));
    });
}

var crawlNext = function() {
    if (urls.length > 0) {
        var url = urls[0];
        urls.splice(0, 1);
        processUrl(url, crawlNext);
    } else {
        phantom.exit();
    }
}

crawlNext();
