``http://mollyproject.org/apps/weather/observation`` - Weather Observation
==========================================================================

Blocks of this type consist of a single weather observation, and attribution for that
observation.

::

    {
        self: "http://mollyproject.org/apps/weather/observation",
        href: "http://localhost:8000/weather/",
        attribution: {
            self: "http://mollyproject.org/common/attribution",
            ...
        },
        observation: {
            wind_speed: "7 mph",
            pressure: "1002 mb",
            obs_time: "2012-10-16 19:00:00+00:00",
            obs_location: "Leek",
            temperature: "5.6 °C",
            wind_direction: "SSW",
            gust_speed: "N/A",
            type: "Clear night"
        }
    }

Blocks of this type are localised according to the Accept-Language headers sent in
the HTTP request. Attribution is a reference to an :doc:`attribution block </api/common/attribution>`.

The observation object consists of the following fields:

+--------------------+---------------------------------------------------------+-----------------------------------+
| Field              | Description                                             | Content type                      |
+====================+=========================================================+===================================+
| ``wind_speed``     | The wind speed at time of observation                   | Free-text string                  |
+--------------------+---------------------------------------------------------+-----------------------------------+
| ``pressure``       | The air pressure at time of observation                 | Free-text string                  |
+--------------------+---------------------------------------------------------+-----------------------------------+
| ``obs_time``       | The time the observation was made                       | ISO-8601 string                   |
+--------------------+---------------------------------------------------------+-----------------------------------+
| ``obs_location``   | The name of the location where the observation was made | Free-text string                  |
+--------------------+---------------------------------------------------------+-----------------------------------+
| ``temperature``    | The temperature at time of observation                  | Free-text string                  |
+--------------------+---------------------------------------------------------+-----------------------------------+
| ``wind_direction`` | The wind direction at time of observation               | Free-text string (compass points) |
+--------------------+---------------------------------------------------------+-----------------------------------+
| ``gust_speed``     | The gusting wind speed                                  | Free-text string                  |
+--------------------+---------------------------------------------------------+-----------------------------------+
| ``type``           | A short description of the current type of weather      | Free-text string                  |
+--------------------+---------------------------------------------------------+-----------------------------------+
