var system = require('system');
var args = system.args;

var fs = require('fs');

var epoch = args[1];
var url = args[2];

var USER_AGENT =
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 ' +
    '(KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36 ' +
    'OPR/29.0.1795.47';

var processUrl = function(url) {
    if (url === undefined || url === null || url.replace(/ /g, '') == '') {
	phantom.exit();
        return;
    }

    var page = require('webpage').create();
    page.settings.userAgent = USER_AGENT;
    page.open('http://www.retailmenot.com/view/' + url, function (status) {
        if (status === 'fail') {
            console.log('Failed to fetch page: ' + url);
	    phantom.exit();
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

	    phantom.exit();
        // Wait randomly between 1 to 3 mins for the page to
        // actually render.
        // Use especially longer timeout since retailmenot seems to have
        // pretty rigorous detection on bots.
        // This delay also serves as a protection so we are not easily
        // detected as a scraper.
        }, 60000 + (120000 * Math.random()));
    });
}

processUrl(url);
