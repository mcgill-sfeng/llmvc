from datetime import date
from assets.BTMS.model.umple import *

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
            # If driver already exists, do nothing or raise error? 
            # Based on feature, creating duplicate is not specified, so assume ignore.
            return
        # Create and add new driver
        new_driver = self.btms._model_layer.Driver(name=drivername)
        self.btms.drivers.add(new_driver)

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
            # If route exists, throw error
            raise ValueError("A route with this number already exists. Please use a different number.")
        # Create and add new route
        new_route = self.btms._model_layer.Route(number=number)
        self.btms.routes.add(new_route)

    def create_route_assignment(self, licensePlate: str, route: int, _date: date):
        # Validate vehicle existence
        vehicle = next((v for v in self.btms.vehicles if v.licencePlate == licensePlate), None)
        if vehicle is None:
            raise ValueError("A bus must be specified for the assignment.")
        # Validate route existence
        route_obj = next((r for r in self.btms.routes if r.number == route), None)
        if route_obj is None:
            raise ValueError("A route must be specified for the assignment.")
        # Validate date
        today = date.today()
        delta_days = abs((_date - today).days)
        if delta_days > 365:
            raise ValueError("The date must be within a year from today.")
        # Create and add new assignment
        new_assignment = self.btms._model_layer.RouteAssignment(date=_date)
        new_assignment.bus = vehicle
        new_assignment.route = route_obj
        self.btms.assignments.add(new_assignment)