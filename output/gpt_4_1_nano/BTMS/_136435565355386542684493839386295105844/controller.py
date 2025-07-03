from datetime import date, timedelta
from assets.BTMS.model.umple import *


class BTMSController:
    def __init__(self):
        self.btms = BTMS()

    def create_driver(self, drivername: str):
        # Validate driver name
        if not drivername or drivername.strip() == "":
            raise ValueError("The name of a driver cannot be empty.")
        # Create driver
        self.btms.create_driver(drivername)

    def create_route(self, number: int):
        # Validate route number
        if number <= 0:
            raise ValueError("The number of a route must be greater than zero.")
        if number > 9999:
            raise ValueError("The number of a route cannot be greater than 9999.")
        # Create route
        self.btms.create_route(number)

    def create_route_assignment(self, licensePlate: str, route: int, _date: date):
        # Validate vehicle
        vehicle = self.btms.get_vehicle(licensePlate)
        if vehicle is None:
            raise ValueError("A bus must be specified for the assignment.")
        # Validate route
        route_obj = self.btms.get_route(route)
        if route_obj is None:
            raise ValueError("A route must be specified for the assignment.")
        # Validate date
        today = date(2035, 1, 1)  # As per current system date
        delta_days = abs((_date - today).days)
        if delta_days > 365:
            raise ValueError("The date must be within a year from today.")
        # Create assignment
        self.btms.create_route_assignment(licensePlate, route, _date)