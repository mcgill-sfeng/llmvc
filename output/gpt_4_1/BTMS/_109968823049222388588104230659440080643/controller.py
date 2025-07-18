from datetime import date
from assets.BTMS.model.umple import *


class BTMSController:
    def __init__(self):
        self.btms = BTMS()

    def create_driver(self, drivername: str):
        """
        Creates a new driver with the given name using the BTMS model.
        Raises ValueError if drivername is empty or None.
        """
        if not drivername or not isinstance(drivername, str):
            raise ValueError("Driver name must be a non-empty string.")
        # Assuming BTMS has an add_driver method
        driver = self.btms.add_driver(drivername)
        return driver

    def create_route(self, number: int):
        """
        Creates a new route with the given number using the BTMS model.
        Raises ValueError if number is not a positive integer.
        """
        if not isinstance(number, int) or number <= 0:
            raise ValueError("Route number must be a positive integer.")
        # Assuming BTMS has an add_route method
        route = self.btms.add_route(number)
        return route

    def create_route_assignment(self, licensePlate: str, route: int, _date: date):
        """
        Creates a new route assignment for the given bus (by licensePlate),
        route number, and date using the BTMS model.
        Raises ValueError if any argument is invalid.
        """
        if not licensePlate or not isinstance(licensePlate, str):
            raise ValueError("License plate must be a non-empty string.")
        if not isinstance(route, int) or route <= 0:
            raise ValueError("Route number must be a positive integer.")
        if not isinstance(_date, date):
            raise ValueError("Date must be a datetime.date instance.")
        # Assuming BTMS has an add_route_assignment method
        assignment = self.btms.add_route_assignment(licensePlate, route, _date)
        return assignment