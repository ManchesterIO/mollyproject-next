/* global console, phantom */
var system = require('system');
var fs = require('fs');

/**
 * Wait until the test condition is true or a timeout occurs. Useful for waiting
 * on a server response or for a ui change (fadeIn, etc.) to occur.
 *
 * @param testFx javascript condition that evaluates to a boolean,
 * it can be passed in as a string (e.g.: "1 == 1" or "$('#bar').is(':visible')" or
 * as a callback function.
 * @param onReady what to do when testFx condition is fulfilled,
 * it can be passed in as a string (e.g.: "1 == 1" or "$('#bar').is(':visible')" or
 * as a callback function.
 * @param timeOutMillis the max amount of time to wait. If not specified, 3 sec is used.
 */
function waitFor(testFx, onReady, timeOutMillis) {
    "use strict";

    var maxtimeOutMillis = timeOutMillis ? timeOutMillis : 3001, //< Default Max Timeout is 3s
        start = new Date().getTime(),
        condition = false,
        interval = setInterval(function() {
            if ( (new Date().getTime() - start < maxtimeOutMillis) && !condition ) {
                // If not time-out yet and condition not yet fulfilled
                condition = (typeof(testFx) === "string" ? eval(testFx) : testFx()); //< defensive code
            } else {
                if(!condition) {
                    // If condition still not fulfilled (timeout but condition is 'false')
                    console.log("'waitFor()' timeout");
                    phantom.exit(1);
                } else {
                    // Condition fulfilled (timeout and/or condition is 'true')
                    typeof(onReady) === "string" ? eval(onReady) : onReady(); //< Do what it's supposed to do once the condition is fulfilled
                    clearInterval(interval); //< Stop this interval
                }
            }
        }, 100); //< repeat check every 100ms
}

var page = require('webpage').create();

// Route "console.log()" calls from within the Page context to the main Phantom context (i.e. current "this")
page.onConsoleMessage = function(msg) {
    "use strict";
    console.log(msg);
};

var relativeScriptPath = require('system').args[0];
var absoluteScriptPath = fs.absolute(relativeScriptPath);
var absoluteScriptDir = absoluteScriptPath.substring(0, absoluteScriptPath.lastIndexOf('/'));

page.open(absoluteScriptDir + fs.separator + "TestRunner.html", function(status){
    "use strict";
    if (status !== "success") {
        console.log("Unable to access network");
        phantom.exit(1);
    } else {
        waitFor(function(){
            return page.evaluate(function(){
                return document.body.querySelector('.results');

            });
        }, function(){
            var failures = page.evaluate(function(){
                var failures = 0;
                var suites = document.querySelectorAll('.suite');
                for (var i = 0; i < suites.length; ++i) {
                    console.log(suites[i].querySelector('.description').innerText);
                    console.log('-----------------------------------------------');
                    var specs = suites[i].querySelectorAll('.specSummary');
                    for (var j = 0; j < specs.length; ++j) {
                        var failed = specs[j].classList.contains('failed');
                        if (failed) {
                            ++failures;
                            console.log("FAILED: " + specs[j].querySelector('.description').innerText);
                        } else {
                            console.log("Success: " + specs[j].querySelector('.description').innerText);
                        }
                    }
                    console.log('');
                }
                return failures;
            });
            phantom.exit(failures ? 1 : 0);
        });
    }
});
