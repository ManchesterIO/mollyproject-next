require(['molly/map', 'vendors/leaflet'], function(molly_map, L) {
    "use strict";

    var MapTest = new TestCase('MapTest', {

        setUp: function() {
            sinon.spy(L, 'map');
        },

        tearDown: function() {
            L.map.restore();
        },

        testMapLoadedCorrectly: function() {
            /*:DOC elem = <div id="map" data-point-of-interest-coordinates="54.0,-12.6"></div>*/
            molly_map(this.elem);

            assertTrue(L.map.called);
            assertTrue(L.map.calledWith(this.elem));
        }

    });

});
