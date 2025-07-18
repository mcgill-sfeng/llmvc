from datetime import date
from assets.BTMS.model.umple import *

class BTMSController:
    def __init__(self):
        self.btms = BTMS()

    def create_driver(self, drivername: str):
        # Create a new Driver with the given name
        self.btms.addDriver(drivername)

    def create_route(self, number: int):
        # Validate route number
        if not isinstance(number, int):
            raise ValueError("Route number must be an integer.")
        if number < 1 or number > 9999:
            raise ValueError("Route number must be between 1 and 9999.")
        # Create a new Route with the given number
        self.btms.addRoute(number)

    def create_route_assignment(self, licensePlate: str, route: int, _date: date):
        # Validate date: must be within one year from today
        today = date.today()
        delta_days = (_date - today).days
        if delta_days < 0 or delta_days > 365:
            raise ValueError("Date must be within one year from today.")
        # Create a new RouteAssignment with the specified bus, route, and date
        self.btms.addRouteAssignment(licensePlate, route, _date)