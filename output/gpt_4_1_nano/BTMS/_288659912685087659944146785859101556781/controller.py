from datetime import date
from assets.BTMS.model.umple import *


class BTMSController:
    def __init__(self):
        self.btms = BTMS()

    def create_driver(self, drivername: str):
        # Validate the driver name
        if not drivername or drivername.strip() == "":
            raise ValueError("The name of a driver cannot be empty.")
        # Add driver to BTMS
        self.btms.addDriver1(drivername)

    def create_route(self, number: int):
        # Validate route number
        if number <= 0:
            raise ValueError("The number of a route must be greater than zero.")
        if number > 9999:
            raise ValueError("The number of a route cannot be greater than 9999.")
        # Check for existing route with same number
        existing_index = self.btms.indexOfRoute(Route(number, self.btms))
        if existing_index != -1:
            raise ValueError("A route with this number already exists. Please use a different number.")
        # Add route
        self.btms.addRoute1(number)

    def create_route_assignment(self, licensePlate: str, route: int, _date: date):
        # Validate vehicle
        vehicle_index = self.btms.indexOfVehicle(BusVehicle(licensePlate, self.btms))
        if vehicle_index == -1:
            raise ValueError("A bus must be specified for the assignment.")
        vehicle = self.btms.getVehicle(vehicle_index)

        # Validate route
        route_obj = None
        route_index = self.btms.indexOfRoute(Route(route, self.btms))
        if route_index == -1:
            # If route does not exist, create it
            self.create_route(route)
            route_index = self.btms.indexOfRoute(Route(route, self.btms))
        route_obj = self.btms.getRoute(route_index)

        # Validate date: within one year from today
        today = date.today()
        delta_days = abs((_date - today).days)
        if delta_days > 365:
            raise ValueError("The date must be within a year from today.")

        # Create assignment
        self.btms.addAssignment1(_date, vehicle, route_obj)