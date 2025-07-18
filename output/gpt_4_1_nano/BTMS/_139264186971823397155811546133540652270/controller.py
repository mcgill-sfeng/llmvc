from datetime import date, timedelta
from assets.BTMS.model.ecore import *

class BTMSController:
    def __init__(self):
        self.btms = BTMS()

    def create_driver(self, drivername: str):
        # Create a new Driver with the given name and a unique ID
        # Assuming the model layer's createDriver method takes a name and auto-generates an ID
        self.btms.createDriver(drivername)

    def create_route(self, number: int):
        # Validate route number: must be an integer between 1 and 9999
        if not isinstance(number, int):
            raise ValueError("Route number must be an integer.")
        if not (1 <= number <= 9999):
            raise ValueError("Route number must be between 1 and 9999.")
        # Create the route
        self.btms.createRoute(number)

    def create_route_assignment(self, licensePlate: str, route: int, _date: date):
        # Validate date: must be within one year from today
        today = date.today()
        one_year_later = today + timedelta(days=365)
        if not (today <= _date <= one_year_later):
            raise ValueError("Date must be within one year from today.")
        # Validate licensePlate: non-empty string
        if not isinstance(licensePlate, str) or not licensePlate.strip():
            raise ValueError("License plate must be a non-empty string.")
        # Validate route number
        if not isinstance(route, int):
            raise ValueError("Route must be an integer.")
        if not (1 <= route <= 9999):
            raise ValueError("Route number must be between 1 and 9999.")
        # Create the route assignment
        self.btms.createRouteAssignment(licensePlate, route, _date)