from datetime import date, timedelta
from assets.BTMS.model.ecore import *

class BTMSController:
    def __init__(self):
        self.btms = BTMS()

    def create_driver(self, drivername: str):
        # Validate the driver name
        if not drivername or drivername.strip() == "":
            raise ValueError("The name of a driver cannot be empty.")
        # Check if a driver with the same name already exists
        existing_driver = next((d for d in self.btms.drivers if d.name == drivername), None)
        if existing_driver:
            # If driver exists, do nothing or raise error? Based on test, probably do nothing
            return
        # Create and add new driver
        new_driver = Driver(name=drivername, schedules=[])
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
        existing_route = next((r for r in self.btms.routes if r.number == number), None)
        if existing_route:
            raise ValueError("A route with this number already exists. Please use a different number.")
        # Create and add new route
        new_route = Route(number=number, assignments=[])
        self.btms.routes.append(new_route)

    def create_route_assignment(self, licensePlate: str, route: int, _date: date):
        # Validate vehicle existence
        vehicle = next((v for v in self.btms.vehicles if v.licencePlate == licensePlate), None)
        if vehicle is None:
            raise ValueError("A bus must be specified for the assignment.")
        # Validate route existence
        route_obj = next((r for r in self.btms.routes if r.number == route), None)
        if route_obj is None:
            raise ValueError("A route must be specified for the assignment.")
        # Validate date: within one year from today
        today = date.today()
        delta_days = abs((_date - today).days)
        if delta_days > 365:
            raise ValueError("The date must be within a year from today.")
        # Check if an assignment already exists for this vehicle on this date
        existing_assignment = next(
            (a for a in self.btms.assignments if a.bus.licencePlate == licensePlate and a.date == _date),
            None
        )
        if existing_assignment:
            # Depending on system design, may prevent duplicate assignments
            # For safety, let's prevent duplicates
            raise ValueError("This vehicle already has an assignment on this date.")
        # Create new assignment
        new_assignment = RouteAssignment(date=_date, bus=vehicle, route=route_obj, schedules=[])
        self.btms.assignments.append(new_assignment)
        # Link assignment to vehicle
        vehicle.assignments.append(new_assignment)
        # Link assignment to route
        route_obj.assignments.append(new_assignment)