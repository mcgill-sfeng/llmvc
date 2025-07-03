from datetime import date, timedelta
from assets.BTMS.model.ecore import *

class BTMSController:
    def __init__(self):
        self.btms = BTMS()

    def create_driver(self, drivername: str):
        if not drivername or drivername.strip() == "":
            raise Exception("The name of a driver cannot be empty.")
        # Check for duplicate names if needed (not specified in requirements)
        driver = Driver(name=drivername, schedules=[])
        if not hasattr(self.btms, "drivers") or self.btms.drivers is None:
            self.btms.drivers = []
        self.btms.drivers.append(driver)
        return driver

    def create_route(self, number: int):
        # Validate number
        if number <= 0:
            raise Exception("The number of a route must be greater than zero.")
        if number > 9999:
            raise Exception("The number of a route cannot be greater than 9999.")
        # Check for duplicate route number
        if not hasattr(self.btms, "routes") or self.btms.routes is None:
            self.btms.routes = []
        for route in self.btms.routes:
            if route.number == number:
                raise Exception("A route with this number already exists. Please use a different number.")
        route = Route(number=number, assignments=[])
        self.btms.routes.append(route)
        return route

    def create_route_assignment(self, licensePlate: str, route: int, _date: date):
        # Validate bus vehicle
        if not hasattr(self.btms, "vehicles") or self.btms.vehicles is None:
            self.btms.vehicles = []
        bus = None
        for v in self.btms.vehicles:
            if v.licencePlate == licensePlate:
                bus = v
                break
        if bus is None:
            raise Exception("A bus must be specified for the assignment.")

        # Validate route
        if not hasattr(self.btms, "routes") or self.btms.routes is None:
            self.btms.routes = []
        route_obj = None
        for r in self.btms.routes:
            if r.number == route:
                route_obj = r
                break
        if route_obj is None:
            raise Exception("A route must be specified for the assignment.")

        # Validate date: must be within a year from today (either direction)
        today = date.today()
        delta = abs((_date - today).days)
        if delta > 365:
            raise Exception("The date must be within a year from today.")

        # Create assignment
        assignment = RouteAssignment(date=_date, bus=bus, route=route_obj, schedules=[])
        if not hasattr(self.btms, "assignments") or self.btms.assignments is None:
            self.btms.assignments = []
        self.btms.assignments.append(assignment)
        # Add to bus and route as well
        if not hasattr(bus, "assignments") or bus.assignments is None:
            bus.assignments = []
        bus.assignments.append(assignment)
        if not hasattr(route_obj, "assignments") or route_obj.assignments is None:
            route_obj.assignments = []
        route_obj.assignments.append(assignment)
        return assignment