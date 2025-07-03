from datetime import date, timedelta
from assets.BTMS.model.umple import *


class BTMSController:
    def __init__(self):
        self.btms = BTMS()

    def create_driver(self, drivername: str):
        # Validate driver name
        if not drivername or drivername.strip() == "":
            raise Exception("The name of a driver cannot be empty.")
        # Create driver
        self.btms.createDriver(drivername)

    def create_route(self, number: int):
        # Validate route number
        if not isinstance(number, int):
            raise Exception("Route number must be an integer.")
        if number <= 0:
            raise Exception("The number of a route must be greater than zero.")
        if number > 9999:
            raise Exception("The number of a route cannot be greater than 9999.")
        # Create route
        self.btms.createRoute(number)

    def create_route_assignment(self, licensePlate: str, route: int, _date: date):
        # Validate vehicle existence
        vehicle = self.btms.getVehicle(licensePlate)
        if vehicle is None:
            raise Exception("A bus must be specified for the assignment.")
        # Validate route existence
        route_obj = self.btms.getRoute(route)
        if route_obj is None:
            raise Exception("A route must be be specified for the assignment.")
        # Validate date
        today = date.today()
        one_year_later = today + timedelta(days=365)
        if _date < today or _date > one_year_later:
            raise Exception("The date must be within a year from today.")
        # Create route assignment
        self.btms.createRouteAssignment(licensePlate, route, _date)