define(['vendors/geoPosition'], function(geoPosition) {
    "use strict";

    var NearbySearch = function(elem) {

        var nearbySearch = this;
        var link = elem.querySelector('button');

        var determineUrl = function(lat, lon) {
            return link.dataset.href.replace("{lat}", lat).replace("{lon}", lon);
        };

        var handleNearbySearchClick = function(ev) {
            link.disabled = true;
            link.innerText = 'Determining your location';
            link.classList.add('loading');
            geoPosition.getCurrentPosition(
                function(position) {
                    nearbySearch.setWindowLocation(determineUrl(position.coords.latitude, position.coords.longitude));
                },
                function(err) {
                    link.classList.remove('loading');
                    link.classList.add('failed');
                    link.innerText = 'Failed to determine your location';
                });
        };

        if (geoPosition.init()) {
            elem.style.display = 'block';
            link.addEventListener('click', handleNearbySearchClick);
        }
    };
    NearbySearch.prototype.setWindowLocation = function(url) {
        window.location = url;
    };

    return function(elem) { return new NearbySearch(elem); };
});