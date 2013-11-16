define(['vendors/leaflet', 'config/static-base', 'css!vendor-styles/leaflet'], function(L, staticBase) {
    "use strict";

    L.Icon.Default.imagePath = staticBase + "img/leaflet/";

    var addPreIe8StylesIfNeeded = function() {
        if (window.attachEvent && !window.addEventListener) {
            require(['css!vendor-styles/leaflet.ie'], function() { });
        }
    };

    var Map = function(elem) {
        var coords = elem.dataset.pointOfInterestCoordinates.split(',').map(parseFloat);
        var map = L.map(elem).setView(coords, 16);

        L.tileLayer('http://{s}.mqcdn.com/tiles/1.0.0/osm/{z}/{x}/{y}.png', {
            maxZoom: 18,
            attribution: 'Data, imagery and map information provided by <a href="http://open.mapquest.co.uk" target="_blank">MapQuest</a>, <a href="http://www.openstreetmap.org/" target="_blank">OpenStreetMap</a> and contributors.',
            subdomains: ['otile1','otile2','otile3','otile4']
        }).addTo(map);

        L.marker(coords).addTo(map);
    };

    addPreIe8StylesIfNeeded();

    return function(elem) {
        return new Map(elem);
    };

});