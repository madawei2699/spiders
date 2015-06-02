var system = require('system');
var args = system.args;

var fs = require('fs');

var urls = fs.read('/home/gjoliver/urls/retailmenot-url').split('\n');

var epoch = args[1];

var processUrl = function(url, next) {
    if (url.replace(/ /g, '') == '') {
        next.apply();
        return;
    }

    var page = require('webpage').create();
    page.open('http://www.retailmenot.com/view/' + url, function (status) {
        if (status === 'fail') {
            console.log('Failed to fetch page: ' + url);
            next.apply();
            return;
        }

        window.setTimeout(function () {
            console.log('Saving page: ' + url);

            var uid = url;
            fs.write('/home/gjoliver/archive/retailmenot/' +
                     epoch + '/' + uid.toLowerCase(),
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
    if (urls.length > 0) {
        var url = urls[0];
        urls.splice(0, 1);
        processUrl(url, crawlNext);
    } else {
        phantom.exit();
    }
}

crawlNext();
