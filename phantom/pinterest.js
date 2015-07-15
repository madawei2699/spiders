var system = require('system');
var args = system.args;

var fs = require('fs');

var uids = fs.read('/home/gjoliver/urls/uid-list-pinterest').split('\n');

var epoch = args[1];

var processUid = function(uid, next) {
    if (uid.replace(/ /g, '') == '') {
        next.apply();
        return;
    }

    var url = 'https://www.pinterest.com/' + uid + '/';

    var page = require('webpage').create();
    page.open(url, function (status) {
        if (status === 'fail') {
            console.log('Failed to fetch page: ' + uid);
            next.apply();
            return;
        }

        window.setTimeout(function () {
            console.log('Saving page: ' + uid);

            fs.write('/home/gjoliver/archive/pinterest/' +
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
