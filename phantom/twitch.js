var system = require('system');
var args = system.args;

var fs = require('fs');

var epoch = args[1];
var uid = args[2];

var processUid = function(uid) {
    if (uid === undefined || uid === null || uid.replace(/ /g, '') == '') {
        phantom.exit();
        return;
    }

    var url = 'https://www.twitch.tv/directory/game/' + uid;

    var page = require('webpage').create();
    page.open(url, function (status) {
        if (status === 'fail') {
            console.log('Failed to fetch page: ' + uid);
            phantom.exit();
            return;
        }

        window.setTimeout(function () {
            console.log('Saving page: ' + uid);

            fs.write('/archd/archive/twitch/' +
                     epoch + '/' + uid.toLowerCase(),
                     page.content,
                     'w');
            page.close();

            phantom.exit();
        // Wait randomly between 20 to 30 seconds for the page to
        // actually render.
        // This delay also serves as a protection so we are not easily
        // detected as a scraper.
        }, 20000 + (10000 * Math.random()));
    });
}

processUid(uid);
