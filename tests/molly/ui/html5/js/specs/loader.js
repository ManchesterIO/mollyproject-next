define('molly/dummy', ['vendors/signals'], function(signals) {
    "use strict";

    var loadSignal = new signals.Signal();

    loadSignal.dispatch.signal = loadSignal;

    return loadSignal.dispatch;
});

define(['molly/loader', 'molly/dummy'], function(loader, dummy) {
    "use strict";

    describe("the correct modules are pulled in from the DOM", function() {

        var div;

        beforeEach(function(){
            div = document.createElement('div');
            div.dataset.mollyModule = 'dummy';
            document.querySelector('body').appendChild(div);
        });

        afterEach(function(){
            div.parentNode.removeChild(div);
        });

        it("calls init on the correct module", function() {

            var calledElem;

            runs(function() {
                dummy.signal.add(function(elem) {
                    calledElem = elem;
                });
                loader.init();
            });

            waitsFor(function() {
                return calledElem !== undefined;
            });

            runs(function() {
                expect(calledElem).toBe(div);
            });
        });
    });

});
