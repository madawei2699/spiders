var system = require('system');
var args = system.args;

var fs = require('fs');

var epoch = args[1];
var account = args[2];
var uid = args[3];

var processUid = function(uid) {
    if (uid === undefined || uid === null || uid.replace(/ /g, '') == '') {
        phantom.exit();
        return;
    }

    var url = 'https://instagram.com' + uid + '?hl=en';

    var page = require('webpage').create();
    page.open(url, function (status) {
        if (status === 'fail') {
            console.log('Failed to fetch page: ' + uid);
            phantom.exit();
            return;
        }

        window.setTimeout(function () {
            console.log('Saving page: ' + account + ' ' + uid);

            fs.write('/archd/archive/instagram_pics/' +
                     epoch + '/' + account + uid.replace(/\//g, '-'),
                     page.content,
                     'w');
            page.close();

            phantom.exit();
        // Wait randomly between 3 to 10 seconds for the page to
        // actually render.
        // This delay also serves as a protection so we are not easily
        // detected as a scraper.
        }, 3000 + (7000 * Math.random()));
    });
}

processUid(uid);
