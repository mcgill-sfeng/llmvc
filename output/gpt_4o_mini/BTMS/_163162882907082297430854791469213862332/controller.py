from datetime import date
from assets.BTMS.model.ecore import *


class BTMSController:
    def __init__(self):
        self.btms = BTMS()

    def create_driver(self, drivername: str):
        """Creates a new driver in the system."""
        if not drivername:
            raise ValueError("Driver name cannot be empty.")
        driver_id = self.btms.add_driver(drivername)
        return driver_id

    def create_route(self, number: int):
        """Creates a new route in the system."""
        if number <= 0:
            raise ValueError("Route number must be a positive integer.")
        route_id = self.btms.add_route(number)
        return route_id

    def create_route_assignment(self, licensePlate: str, route: int, _date: date):
        """Assigns a route to a vehicle on a specific date."""
        if not licensePlate:
            raise ValueError("License plate cannot be empty.")
        if route <= 0:
            raise ValueError("Route number must be a positive integer.")
        if _date > date.today():
            raise ValueError("Date cannot be in the future.")
        
        assignment_id = self.btms.assign_route_to_vehicle(licensePlate, route, _date)
        return assignment_id