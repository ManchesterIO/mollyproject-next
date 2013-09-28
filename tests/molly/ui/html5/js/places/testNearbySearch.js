require(['molly/places/nearby-search'], function(nearbySearch) {
    "use strict";

    var PlacesNearbySearchTest = new TestCase('PlacesNearbySearchTest', {

        testDivIsMadeVisible: function() {
            /*:DOC elem = <div><a href="/nearby/{lat},{lon}/"></a></div>*/
            this.elem.style.display = 'none';
            nearbySearch(this.elem);
            assertEquals('block', this.elem.style.display);
        }

    });

});