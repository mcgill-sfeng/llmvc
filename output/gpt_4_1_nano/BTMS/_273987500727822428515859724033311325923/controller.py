from datetime import date, timedelta
from assets.BTMS.model.umple import *

class BTMSController:
    def __init__(self):
        self.btms = BTMS()

    def create_driver(self, drivername: str):
        # Validate name
        if not drivername or drivername.strip() == "":
            raise Exception("The name of a driver cannot be empty.")
        # Check if driver with same name exists
        for driver in self.btms.getDrivers():
            if driver.getName() == drivername:
                # Driver already exists, do nothing or raise error? 
                # Based on test, creating same driver again is not specified, so ignore.
                return
        # Add new driver
        self.btms.addDriver1(drivername)

    def create_route(self, number: int):
        # Validate number
        if not isinstance(number, int):
            raise Exception("Route number must be an integer.")
        if number <= 0:
            raise Exception("The number of a route must be greater than zero.")
        if number > 9999:
            raise Exception("The number of a route cannot be greater than 9999.")
        # Check if route with same number exists
        for route in self.btms.getRoutes():
            if route.getNumber() == number:
                raise Exception("A route with this number already exists. Please use a different number.")
        # Add new route
        self.btms.addRoute1(number)

    def create_route_assignment(self, licensePlate: str, route: int, _date: date):
        # Validate vehicle
        vehicle = None
        for v in self.btms.getVehicles():
            if v.getLicencePlate() == licensePlate:
                vehicle = v
                break
        if vehicle is None:
            raise Exception("A bus must be specified for the assignment.")
        # Validate route
        route_obj = None
        for r in self.btms.getRoutes():
            if r.getNumber() == route:
                route_obj = r
                break
        if route_obj is None:
            raise Exception("A route must be be specified for the assignment.")
        # Validate date: within one year from today
        today = date.today()
        delta = _date - today
        if delta.days < 0 or delta.days > 365:
            raise Exception("The date must be within a year from today.")
        # Create assignment
        self.btms.addAssignment1(_date, vehicle, route_obj)