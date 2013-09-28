define(['molly/map', 'vendors/leaflet', 'sinon'], function(molly_map, L, sinon) {
    "use strict";

    describe("maps appear on the page", function() {

        beforeEach(function(){
            sinon.spy(L, 'map');
        });

        afterEach(function(){
            L.map.restore();
        });

        it("loads the map correctly", function() {
            var div = document.createElement('div');
            div.dataset.pointOfInterestCoordinates = "54.0,-12.6";

            molly_map(div);

            expect(L.map.called).toBeTruthy();
            expect(L.map.calledWith(div)).toBeTruthy();
        });
    });

});
