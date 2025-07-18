from datetime import date, timedelta
from assets.BTMS.model.ecore import *

class BTMSController:
    def __init__(self):
        self.btms = BTMS()

    def create_driver(self, drivername: str):
        if drivername is None or drivername.strip() == "":
            raise Exception("The name of a driver cannot be empty.")
        # Check for duplicate names if needed (not specified in requirements)
        driver = self.btms.Driver()
        driver.name = drivername
        self.btms.drivers.append(driver)

    def create_route(self, number: int):
        if not isinstance(number, int):
            raise Exception("The number of a route must be an integer.")
        if number <= 0:
            raise Exception("The number of a route must be greater than zero.")
        if number > 9999:
            raise Exception("The number of a route cannot be greater than 9999.")
        # Check for duplicate route number
        for route in self.btms.routes:
            if route.number == number:
                raise Exception("A route with this number already exists. Please use a different number.")
        route = self.btms.Route()
        route.number = number
        self.btms.routes.append(route)

    def create_route_assignment(self, licensePlate: str, route: int, _date: date):
        # Find bus vehicle by license plate
        bus = None
        for v in self.btms.vehicles:
            if v.licencePlate == licensePlate:
                bus = v
                break
        if bus is None:
            raise Exception("A bus must be specified for the assignment.")

        # Find route by number
        route_obj = None
        for r in self.btms.routes:
            if r.number == route:
                route_obj = r
                break
        if route_obj is None:
            raise Exception("A route must be specified for the assignment.")

        # Date validation: must be within a year from today (future or past)
        today = date.today()
        delta = abs((_date - today).days)
        if delta > 365:
            raise Exception("The date must be within a year from today.")

        # Create assignment
        assignment = self.btms.RouteAssignment()
        assignment.bus = bus
        assignment.route = route_obj
        assignment.date = _date
        self.btms.assignments.append(assignment)
        # Add assignment to bus and route (if model does not do this automatically)
        if hasattr(bus, "assignments"):
            bus.assignments.append(assignment)
        if hasattr(route_obj, "assignments"):
            route_obj.assignments.append(assignment)