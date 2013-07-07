require(['molly/map', 'vendors/leaflet'], function(molly_map, L) {
    "use strict";

    var MapTest = new TestCase('MapTest', {

        setUp: function() {
            sinon.spy(L, 'Map');
        },

        tearDown: function() {
            L.Map.restore();
        },

        testMapLoadedCorrectly: function() {
            /*:DOC elem = <div id="map"></div>*/
            molly_map.init(this.elem);

            assertTrue(L.Map.called);
        }
    });

});
