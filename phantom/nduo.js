var system = require('system');
var args = system.args;

var fs = require('fs');

var epoch = args[1];
var url = args[2];

var processUrl = function(url) {
    if (url === undefined || url === null || url.replace(/ /g, '') == '') {
	phantom.exit();
        return;
    }

    var page = require('webpage').create();
    page.open(url, function (status) {
        if (status === 'fail') {
            console.log('Failed to fetch page: ' + url);
	    phantom.exit();
            return;
        }

        window.setTimeout(function () {
            console.log('Saving page: ' + url);

            var uid = url
                .replace('http://www.nduoa.com/apk/detail/', '')
                .replace('http://www.nduoa.com/package/detail/')
                .replace('undefined', '');
            fs.write('/archd/archive/nduo/' +
                     epoch + '/' + uid.toLowerCase(),
                     page.content,
                     'w');
            page.close();

	    phantom.exit();
        // Wait randomly between 3 to 10 seconds for the page to
        // actually render.
        // This delay also serves as a protection so we are not easily
        // detected as a scraper.
        }, 3000 + (12000 * Math.random()));
    });
}

processUrl(url);
