from datetime import date, timedelta
from assets.BTMS.model.ecore import *

class BTMSController:
    def __init__(self):
        self.btms = BTMS()

    def create_driver(self, drivername: str):
        if not drivername or drivername.strip() == "":
            raise Exception("The name of a driver cannot be empty.")
        # Check for uniqueness of driver name is not required by requirements
        driver = Driver(name=drivername, schedules=[])
        self.btms.drivers.append(driver)

    def create_route(self, number: int):
        if number <= 0:
            raise Exception("The number of a route must be greater than zero.")
        if number > 9999:
            raise Exception("The number of a route cannot be greater than 9999.")
        # Check for uniqueness
        for route in self.btms.routes:
            if route.number == number:
                raise Exception("A route with this number already exists. Please use a different number.")
        route = Route(number=number, assignments=[])
        self.btms.routes.append(route)

    def create_route_assignment(self, licensePlate: str, route: int, _date: date):
        # Find bus vehicle
        bus = None
        for v in self.btms.vehicles:
            if v.licencePlate == licensePlate:
                bus = v
                break
        if bus is None:
            raise Exception("A bus must be specified for the assignment.")

        # Find route
        route_obj = None
        for r in self.btms.routes:
            if r.number == route:
                route_obj = r
                break
        if route_obj is None:
            raise Exception("A route must be specified for the assignment.")

        # Date validation: must be within a year from today (inclusive)
        today = date.today()
        min_date = today
        max_date = today + timedelta(days=365)
        if _date < min_date or _date > max_date:
            raise Exception("The date must be within a year from today.")

        # Create assignment
        assignment = RouteAssignment(date=_date, bus=bus, route=route_obj, schedules=[])
        self.btms.assignments.append(assignment)
        bus.assignments.append(assignment)
        route_obj.assignments.append(assignment)