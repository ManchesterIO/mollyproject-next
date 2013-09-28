define(['molly/places/nearby-search', 'sinon', 'vendors/geoPosition'], function(nearbySearch, sinon, geoPosition) {
    "use strict";

    describe("nearby search is available on devices with geolocation", function() {

        var div, link, setWindowLocation;

        beforeEach(function() {
            div = document.createElement('div');
            div.style.display = 'none';

            link = document.createElement('button');
            link.dataset.href = '/places/{lat},{lon}';
            div.appendChild(link);

            sinon.stub(geoPosition, "init");
            sinon.stub(geoPosition, "getCurrentPosition");
            setWindowLocation = undefined;
            geoPosition.init.returns(true);
        });

        afterEach(function() {
            geoPosition.init.restore();
            geoPosition.getCurrentPosition.restore();
            if (setWindowLocation !== undefined ) {
                setWindowLocation.restore();
            }
        });

        it("shows the nearby link on devices with JavaScript", function() {
            nearbySearch(div);
            expect(div.style.display).toBe('block');
        });

        it("does not show the nearby link on devices without JavaScript", function() {
            geoPosition.init.returns(false);
            nearbySearch(div);
            expect(div.style.display).toBe('none');
        });

        it("changes to a loading spinner when clicked on", function() {
            nearbySearch(div);
            link.dispatchEvent(new window.MouseEvent('click'));
            expect(link.classList.contains('loading')).toBeTruthy();
            expect(link.innerText).toBe("Determining your location");
            expect(link.disabled).toBeTruthy();
        });

        it("when geolocation returns result, user is navigated to page", function() {
            geoPosition.getCurrentPosition.callsArgWith(0, {coords: {latitude: 12.3, longitude: 45.6}});
            setWindowLocation = sinon.stub(nearbySearch(div), 'setWindowLocation');
            link.dispatchEvent(new window.MouseEvent('click'));
            expect(setWindowLocation.calledWith('/places/12.3,45.6')).toBeTruthy();
        });

        it("shows an error message when geolocation fails", function() {
            geoPosition.getCurrentPosition.callsArgWith(1, {code: 1});
            nearbySearch(div);
            link.dispatchEvent(new window.MouseEvent('click'));
            expect(link.classList.contains('loading')).toBeFalsy();
            expect(link.classList.contains('failed')).toBeTruthy();
            expect(link.innerText).toBe("Failed to determine your location");
        });
    });

});