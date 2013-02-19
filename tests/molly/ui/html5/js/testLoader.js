define('molly/dummy', ['vendors/signals'], function(signals) {
    "use strict";

    var loadSignal = new signals.Signal();

    return {
        init: function (elem) {
            loadSignal.dispatch(elem);
        },
        loadSignal: loadSignal
    };
});

require(['molly/loader', 'molly/dummy'], function(loader, dummy) {
    "use strict";

    var LoaderTest = new AsyncTestCase('LoaderTest', {

        testLoaderLoadsModulesFromBody: function(queue) {
            var div = document.createElement('div');
            div.id = 'test';
            div.dataset.mollyModule = 'dummy';
            document.getElementsByTagName('body')[0].appendChild(div);

            queue.call(function(callbacks) {
                loader.init(document.getElementById('test'));
                dummy.loadSignal.add(callbacks.add(function(elem) {
                    assertEquals(document.getElementById('test'), elem);
                }));
            });

        }
    });

});

