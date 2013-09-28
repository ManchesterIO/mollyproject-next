require(['molly/places/nearby-search'], function(nearbySearch) {
    "use strict";

    var div;

    beforeEach(function(){
        div = document.createElement('div');
        var a = document.createElement('a');
        a.href = '/places/{lat},{lon}';
        div.appendChild(a);
    });

    describe("nearby search is available on devices with geolocation", function() {
        it("shows the nearby link on devices with JavaScript", function() {
            div.style.display = 'none';
            nearbySearch(div);
            expect(div.style.display).toBe('block');
        });
    });

});