from molly.apps.common.components import Source, Identifier, Attribution
from molly.apps.transport.models import STANOX_NAMESPACE, CRS_NAMESPACE, CallingPoint, TIPLOC_NAMESPACE, CIF_DESCRIPTION_NAMESPACE, ScheduledTrip, Call, CallTime, Route, Service

class CifParser(object):

    _SOURCE_URL = 'cif:'
    _ATTRIBUTION = Attribution(
        attribution_text='Source: RSP',
        attribution_url='http://www.atoc.org/',
        licence_name='Creative Commons Attribution-ShareAlike',
        licence_url='http://creativecommons.org/licenses/by-sa/1.0/legalcode'
    )

    def import_from_file(self, archive):
        self._reset_state()
        self._parse_mca_file(archive)

    def _reset_state(self):
        self._tiploc_descriptions = {}
        self.tiplocs = []
        self.routes = []
        self._routes = {}
        self.services = []
        self._services = {}
        self.scheduled_trips = []
        self._platform_slugs = set()

    def _parse_mca_file(self, archive):
        handlers = {
            'TI': self._handle_tiploc_insert,
            'BS': self._handle_journey_schedule_start,
            'LO': self._handle_journey_origin,
            'LI': self._handle_journey_call,
            'LT': self._handle_journey_end,
            'ZZ': self._handle_file_end
        }

        self._source = Source(
            url=self._SOURCE_URL,
            version=archive.namelist[0].split('.')[0],
            attribution=self._ATTRIBUTION
        )

        with self._open_mca_file(archive) as mca_file:
            for line in mca_file:
                handler = handlers.get(line[:2])
                if handler is not None:
                    handler(line)

    def _open_mca_file(self, archive):
        mca_filename = filter(lambda fn: fn.endswith('.MCA'), archive.namelist)[0]
        return archive.open(mca_filename)

    def _handle_tiploc_insert(self, line):
        tiploc = line[2:9].strip()
        description = line[18:44].strip().title()

        calling_point = self._build_calling_point(description, tiploc)
        calling_point.identifiers.add(Identifier(namespace=STANOX_NAMESPACE, value=line[44:49]))

        crs_code = line[53:56].strip()
        if crs_code:
            calling_point.identifiers.add(Identifier(namespace=CRS_NAMESPACE, value=line[53:56]))

        self._tiploc_descriptions[tiploc] = description
        self.tiplocs.append(calling_point)

    def _build_calling_point(self, description, tiploc):
        calling_point = CallingPoint()
        calling_point.sources.add(self._source)
        calling_point.identifiers.add(Identifier(namespace=TIPLOC_NAMESPACE, value=tiploc))
        calling_point.identifiers.add(Identifier(namespace=CIF_DESCRIPTION_NAMESPACE, value=description))
        return calling_point

    def _handle_journey_schedule_start(self, line):
        self._current_calling_tiplocs = []
        self._current_scheduled_trip = ScheduledTrip()
        self._current_scheduled_trip.sources.add(self._source)
        self._current_scheduled_trip.slug = '/gb/rail/' + line[3:9]

    def _handle_journey_origin(self, line):
        self._add_tiploc_to_journey(
            tiploc=line[2:9].strip(),
            scheduled_departure_time=line[10:15].strip(),
            public_departure_time=line[15:19].strip(),
            platform=line[19:22].strip(),
            activity=self._get_activity(line[29:41])
        )

    def _handle_journey_call(self, line):
        pass_time = line[20:25].strip()
        if pass_time:
            self._add_tiploc_to_journey(
                tiploc=line[2:9].strip(),
                scheduled_arrival_time=pass_time,
                scheduled_departure_time=pass_time,
                platform=line[33:36].strip(),
                activity=Call.PASS_THROUGH
            )
        else:
            self._add_tiploc_to_journey(
                tiploc=line[2:9].strip(),
                scheduled_arrival_time=line[10:15].strip(),
                scheduled_departure_time=line[15:20].strip(),
                public_arrival_time=line[25:29].strip(),
                public_departure_time=line[29:33].strip(),
                platform=line[33:36].strip(),
                activity=self._get_activity(line[42:54])
            )

    def _handle_journey_end(self, line):
        self._add_tiploc_to_journey(
            tiploc=line[2:9].strip(),
            scheduled_arrival_time=line[10:15].strip(),
            public_arrival_time=line[15:19].strip(),
            platform=line[19:22].strip(),
            activity=self._get_activity(line[25:37])
        )
        route = self._get_route_for_current_journey()
        self._current_scheduled_trip.route_slug = route.slug
        self.scheduled_trips.append(self._current_scheduled_trip)

    def _add_tiploc_to_journey(
            self, tiploc, platform, activity, scheduled_arrival_time=None, public_arrival_time=None,
            scheduled_departure_time=None, public_departure_time=None
    ):
        self._current_calling_tiplocs.append(tiploc)
        calling_point_slug = self._get_calling_point(platform, tiploc)
        self._current_scheduled_trip.calling_points.append(
            Call(
                point_slug=calling_point_slug,
                scheduled_arrival_time=self._convert_to_python_time(scheduled_arrival_time),
                public_arrival_time=self._convert_to_python_time(public_arrival_time),
                scheduled_departure_time=self._convert_to_python_time(scheduled_departure_time),
                public_departure_time=self._convert_to_python_time(public_departure_time),
                activity=activity
            )
        )

    def _convert_to_python_time(self, cif_time):
        if cif_time is None:
            return None
        else:
            s = 30 if cif_time.endswith('H') else 0
            h = int(cif_time[:2])
            m = int(cif_time[2:4])
            return CallTime(h, m, s)

    def _get_activity(self, activity_codes):
        operational = False
        for i in range(0, len(activity_codes), 2):
            activity_code = activity_codes[i:i+2].strip()
            if activity_code in (
                    'A', 'AE', 'BL', 'C', '-D', 'E', 'K', 'KC', 'KE', 'KF', 'KS', 'L', 'N', 'OP', 'OR',
                    'PR', 'RM', 'RR', 'S', '-T', 'TW', '-U', 'W', 'X'
                ):
                operational = True
            else:
                activity = {
                    'D': Call.SET_DOWN_ONLY,
                    'T': Call.NORMAL,
                    'TB': Call.START,
                    'TF': Call.FINISH,
                    'U': Call.PICK_UP_ONLY
                }.get(activity_code)
                if activity is not None:
                    return activity

        if operational:
            return Call.OPERATIONAL_STOP


    def _get_calling_point(self, platform, tiploc):
        if platform:
            platform_slug = '/gb/9400{tiploc}/platform{platform}'.format(
                tiploc=tiploc, platform=platform
            )
            if platform_slug not in self._platform_slugs:
                self._build_platform(platform, platform_slug, tiploc)
            return platform_slug
        else:
            return '/gb/9400{tiploc}/calling_point'.format(tiploc=tiploc)

    def _build_platform(self, platform, platform_slug, tiploc):
        platform_calling_point = self._build_calling_point(
            '{description} Platform {platform}'.format(
                description=self._tiploc_descriptions[tiploc],
                platform=platform
            ), tiploc
        )
        platform_calling_point.slug = platform_slug
        platform_calling_point.parent_slug = '/gb/9400{tiploc}'.format(
            tiploc=tiploc
        )
        self._platform_slugs.add(platform_slug)
        self.tiplocs.append(platform_calling_point)

    def _handle_file_end(self, line):
        pass

    def _get_route_for_current_journey(self):
        route = self._routes.get(tuple(self._current_calling_tiplocs))
        if route is None:
            route = self._build_route()
        return route

    def _build_route(self):
        route = Route()
        route.sources.add(self._source)
        route.slug = '/gb/rail/{origin}-{destination}'.format(
            origin=self._current_calling_tiplocs[0],
            destination=self._current_calling_tiplocs[-1]
        )

        for tiploc in self._current_calling_tiplocs:
            route.calling_points.append(
                '/gb/9400{tiploc}/calling_point'.format(tiploc=tiploc)
            )

        route.headline = self._tiploc_descriptions[self._current_calling_tiplocs[-1]]

        self.routes.append(route)
        self._routes[tuple(self._current_calling_tiplocs)] = route
        service = self._get_service_for_route(route)
        service.routes.add(route.slug)
        route.service_slug = service.slug
        return route

    def _get_service_for_route(self, route):
        service = self._services.get(self._build_service_key_for_current_journey())
        if service is None:
            service = self._build_service(route)
            service.name = '{origin} to {destination}'.format(
                origin=self._tiploc_descriptions[self._current_calling_tiplocs[0]],
                destination=self._tiploc_descriptions[self._current_calling_tiplocs[-1]]
            )
        return service

    def _build_service(self, route):
        service = Service()
        service.sources.add(self._source)
        service.slug = route.slug
        self.services.append(service)
        self._services[self._build_service_key_for_current_journey()] = service
        return service

    def _build_service_key_for_current_journey(self):
        return frozenset({self._current_calling_tiplocs[0], self._current_calling_tiplocs[-1]})

