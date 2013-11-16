define([], function() {
    "use strict";

    return {
        init: function() {
            /*jshint loopfunc:true */
            var mollyElements = document.querySelectorAll('[data-molly-module]');

            for (var i = 0; i < mollyElements.length; ++i) {
                var mollyModule = mollyElements[i].getAttribute('data-molly-module');
                (function (i) {
                    require(['molly/' + mollyModule], function(module) {
                        module(mollyElements[i]);
                    });
                }(i));
            }
        }
    };
});