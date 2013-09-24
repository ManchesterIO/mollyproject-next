require(['molly/map', 'vendors/leaflet'], function(molly_map, L) {
    "use strict";

    var MapTest = new TestCase('MapTest', {

        setUp: function() {
            sinon.stub(L, 'map');
        },

        tearDown: function() {
            L.map.restore();
        },

        testMapLoadedCorrectly: function() {
            /*:DOC elem = <div id="map"></div>*/
            molly_map(this.elem);

            assertTrue(L.map.called);
            assertTrue(L.map.calledWith(this.elem));
        }

    });

});
