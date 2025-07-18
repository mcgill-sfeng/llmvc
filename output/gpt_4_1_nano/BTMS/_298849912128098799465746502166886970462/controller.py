from datetime import date, timedelta
from assets.BTMS.model.ecore import *
from assets.BTMS.model.ecore import *

class BTMSController:
    def __init__(self):
        self.btms = BTMS()

    def create_driver(self, drivername: str):
        # Validate the driver name
        if not drivername or drivername.strip() == "":
            raise ValueError("The name of a driver cannot be empty.")
        # Check if a driver with the same name already exists
        for driver in self.btms.drivers:
            if driver.name == drivername:
                # If exists, do nothing or raise error? Based on tests, probably do nothing
                return
        # Create and add new driver
        new_driver = Driver(name=drivername)
        self.btms.drivers.append(new_driver)

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
        # Create and add new route
        new_route = Route(number=number)
        self.btms.routes.append(new_route)

    def create_route_assignment(self, licensePlate: str, route: int, _date: date):
        # Validate vehicle existence
        vehicle = None
        for v in self.btms.vehicles:
            if v.licencePlate == licensePlate:
                vehicle = v
                break
        if vehicle is None:
            raise ValueError("A bus must be specified for the assignment.")
        # Validate route existence
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
        assignment = RouteAssignment(date=_date, bus=vehicle, route=route_obj)
        self.btms.assignments.append(assignment)
        # Link assignment to vehicle
        if vehicle.assignments is None:
            vehicle.assignments = []
        vehicle.assignments.append(assignment)
        # Link assignment to route
        if route_obj.assignments is None:
            route_obj.assignments = []
        route_obj.assignments.append(assignment)
        # Link assignment to schedules if needed (not specified in creation)
        # No schedules are created here, so skip