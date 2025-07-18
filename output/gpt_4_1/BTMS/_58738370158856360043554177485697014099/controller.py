from datetime import date, timedelta
from assets.BTMS.model.ecore import *

class BTMSController:
    def __init__(self):
        self.btms = BTMS()

    def create_driver(self, drivername: str):
        if not drivername or drivername.strip() == "":
            raise ValueError("The name of a driver cannot be empty.")
        # Check for duplicate driver names (optional, not specified, but model uses unique=True)
        for d in self.btms.drivers:
            if d.name == drivername:
                # Not specified in requirements, so allow duplicate names
                pass
        driver = Driver(name=drivername)
        self.btms.drivers.append(driver)
        return driver

    def create_route(self, number: int):
        if number <= 0:
            raise ValueError("The number of a route must be greater than zero.")
        if number > 9999:
            raise ValueError("The number of a route cannot be greater than 9999.")
        for r in self.btms.routes:
            if r.number == number:
                raise ValueError("A route with this number already exists. Please use a different number.")
        route = Route(number=number)
        self.btms.routes.append(route)
        return route

    def create_route_assignment(self, licensePlate: str, route: int, _date: date):
        # Find bus by licensePlate
        bus = None
        for v in self.btms.vehicles:
            if v.licencePlate == licensePlate:
                bus = v
                break
        if bus is None:
            raise ValueError("A bus must be specified for the assignment.")

        # Find route by number
        route_obj = None
        for r in self.btms.routes:
            if r.number == route:
                route_obj = r
                break
        if route_obj is None:
            raise ValueError("A route must be specified for the assignment.")

        # Date validation: must be within a year from today (inclusive)
        today = date.today()
        min_date = today
        max_date = today + timedelta(days=365)
        if _date < min_date or _date > max_date:
            raise ValueError("The date must be within a year from today.")

        # Create assignment
        assignment = RouteAssignment(date=_date, bus=bus, route=route_obj)
        self.btms.assignments.append(assignment)
        # Link assignment to bus and route
        bus.assignments.append(assignment)
        route_obj.assignments.append(assignment)
        return assignment