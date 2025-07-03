from datetime import date
from assets.BTMS.model.umple import *


class BTMSController:
    def __init__(self):
        self.btms = BTMS()

    def create_driver(self, drivername: str):
        # Validate the driver name
        if not drivername or drivername.strip() == "":
            raise ValueError("The name of a driver cannot be empty.")
        # Check if a driver with this name already exists
        if self.btms.getDriver(self.btms.getDriver, drivername):
            # If exists, do not create a new one, just return or handle as needed
            # For this implementation, assume we do not create duplicates
            return
        # Create and add the driver
        self.btms.addDriver(drivername)

    def create_route(self, number: int):
        # Validate the route number
        if not isinstance(number, int):
            raise ValueError("Route number must be an integer.")
        if number <= 0:
            raise ValueError("The number of a route must be greater than zero.")
        if number > 9999:
            raise ValueError("The number of a route cannot be greater than 9999.")
        # Check if route with this number already exists
        if self.btms.getRoute(self.btms.getRoute, number):
            # Route with this number exists, throw error
            raise ValueError("A route with this number already exists. Please use a different number.")
        # Create and add the route
        self.btms.addRoute(number)

    def create_route_assignment(self, licensePlate: str, route: int, _date: date):
        # Validate vehicle
        vehicle = self.btms.getVehicle(self.btms.getVehicle, licensePlate)
        if vehicle is None:
            raise ValueError("A bus must be specified for the assignment.")
        # Validate route
        route_obj = self.btms.getRoute(self.btms.getRoute, route)
        if route_obj is None:
            raise ValueError("A route must be specified for the assignment.")
        # Validate date: within one year from today
        today = date.today()
        delta_days = abs((_date - today).days)
        if delta_days > 365:
            raise ValueError("The date must be within a year from today.")
        # Create and add the assignment
        self.btms.addAssignment(_date, vehicle, route_obj)