from datetime import date, timedelta
from assets.BTMS.model.ecore import *

class BTMSController:
    def __init__(self):
        self.btms = BTMS()

    def create_driver(self, drivername: str):
        # Validate driver name
        if not drivername or drivername.strip() == "":
            raise ValueError("The name of a driver cannot be empty.")
        # Create and add driver
        driver = Driver(name=drivername, schedules=[])
        self.btms.drivers.append(driver)

    def create_route(self, number: int):
        # Validate route number
        if not isinstance(number, int):
            raise ValueError("Route number must be an integer.")
        if number <= 0:
            raise ValueError("The number of a route must be greater than zero.")
        if number > 9999:
            raise ValueError("The number of a route cannot be greater than 9999.")
        # Check for existing route with same number
        for route in self.btms.routes:
            if route.number == number:
                raise ValueError("A route with this number already exists. Please use a different number.")
        # Create and add route
        route = Route(number=number, assignments=[])
        self.btms.routes.append(route)

    def create_route_assignment(self, licensePlate: str, route: int, _date: date):
        # Validate vehicle
        vehicle = None
        for v in self.btms.vehicles:
            if v.licencePlate == licensePlate:
                vehicle = v
                break
        if vehicle is None:
            raise ValueError("A bus must be specified for the assignment.")
        # Validate route
        route_obj = None
        for r in self.btms.routes:
            if r.number == route:
                route_obj = r
                break
        if route_obj is None:
            raise ValueError("A route must be specified for the assignment.")
        # Validate date: within one year from today
        today = date.today()
        delta_days = abs((_date - today).days)
        if delta_days > 365:
            raise ValueError("The date must be within a year from today.")
        # Create assignment
        assignment = RouteAssignment(date=_date, bus=vehicle, route=route_obj, schedules=[])
        self.btms.assignments.append(assignment)
        # Link assignment to vehicle
        vehicle.assignments.append(assignment)
        # Link assignment to route
        route_obj.assignments.append(assignment)