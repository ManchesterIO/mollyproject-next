import datetime

class Service(object):
    """
    A high level object to encapsulate an item which a user identifies as an individual service,
    e.g., the 216 bus route or the London-Manchester Pendolino service
    """

    def __init__(self):
        self.url = None
        self.mode = None
        self.routes = set()


class Route(object):
    """
    One route which a service operates on - there can be many route variants (e.g., inbound, outbound,
    peak, etc) in a service
    """

    def __init__(self):
        self.url = None
        self.calling_points = []
        self.service_url = None
        self.headline = None
        self.via = None


class ScheduledTrip(object):
    """
    A scheduled trip is a one particular journey on a route which has timings associated with it
    """

    def __init__(self):
        self.url = None
        self.route_url = None
        self.calling_points = []


class Call(object):

    # Activities which can be performed at this call
    NORMAL = 'normal' # passengers are picked up and set down
    PASS_THROUGH = 'pass-through' # passes through a point
    OPERATIONAL_STOP = 'operational-stop' # stops for an operational reason (e.g., change of driver)
    PICK_UP_ONLY = 'pick-up-only' # stops to pick up only
    SET_DOWN_ONLY = 'set-down-only' # stops to set down only
    START = 'start' # journey starts here
    FINISH = 'finish' # journey completes here

    def __init__(self):
        self.point_url = None
        self.scheduled_arrival_time = None
        self.timetabled_arrival_time = None
        self.scheduled_departure_time = None
        self.timetabled_departure_time = None
        self.activity = None


class CallTime(datetime.time):
    """
    A time class which handles the fact that some schedules spread over midnight, e.g., a Friday night service
    might actually happen on Saturday morning
    """

    def __init__(self, *args, **kwargs):
        super(CallTime, self).__init__(*args, **kwargs)
        self.next_day = False


class OperationPeriod(object):
    """
    This defines the period which a scheduled trip can run on. A scheduled trip can have multiple applicable periods,
    this captures an individual one. A period is defined by its start date and end date (either or which can be open
    ended and the covered dates are inclusive), Boolean parameters which indicate which days of the week this runs on
    and a set of excluded dates which this period would normally cover but in this case aren't (e.g., bank holidays)
    """

    def __init__(self):
        self.start_date = None
        self.end_date = None
        self.excluded_dates = set()
        self.monday = False
        self.tuesday = False
        self.wednesday = False
        self.thursday = False
        self.friday = False
        self.saturday = False
        self.sunday = False
