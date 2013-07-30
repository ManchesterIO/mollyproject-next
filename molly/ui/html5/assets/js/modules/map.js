define('molly/map', ['vendors/leaflet'], function(L) {
    "use strict";

    var Map = function(elem) {
        var map = new L.Map(elem);
    };

    return function(elem) {
        return new Map(elem);
    };

});