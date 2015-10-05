var system = require('system');
var args = system.args;

var fs = require('fs');

var uids = fs.read('/home/gjoliver/urls/uid-list-fb').split('\n');

var epoch = args[1];

var processUid = function(uid, next) {
    if (uid.replace(/ /g, '') == '') {
        next.apply();
        return;
    }

    var page = require('webpage').create();
    var url = 'https://www.facebook.com/' + uid + '/likes';
    page.open(url, function (status) {
        if (status === 'fail') {
            console.log('Failed to fetch page: ' + url);
            next.apply();
            return;
        }

        window.setTimeout(function () {
            console.log('Saving page: ' + url);

            fs.write('/archd/archive/fb/' +
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
    if (uids.length > 0) {
        var uid = uids[0];
        uids.splice(0, 1);
        processUid(uid, crawlNext);
    } else {
        phantom.exit();
    }
}

crawlNext();
