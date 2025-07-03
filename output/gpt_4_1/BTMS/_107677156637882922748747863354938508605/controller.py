from datetime import date, timedelta
from assets.BTMS.model.umple import *

class BTMSController:
    def __init__(self):
        self.btms = BTMS()

    def create_driver(self, drivername: str):
        # Validate input
        if not isinstance(drivername, str) or not drivername.strip():
            raise ValueError("Driver name must be a non-empty string.")
        if Driver.hasWithName(drivername):
            raise ValueError(f"Driver with name '{drivername}' already exists.")
        # Create and add driver
        driver = self.btms.addDriver(drivername)
        return driver

    def create_route(self, number: int):
        # Validate input
        if not isinstance(number, int):
            raise ValueError("Route number must be an integer.")
        if not (1 <= number <= 9999):
            raise ValueError("Route number must be between 1 and 9999.")
        if Route.hasWithNumber(number):
            raise ValueError(f"Route with number '{number}' already exists.")
        # Create and add route
        route = self.btms.addRoute(number)
        return route

    def create_route_assignment(self, licensePlate: str, route: int, _date: date):
        # Validate licensePlate
        if not isinstance(licensePlate, str) or not licensePlate.strip():
            raise ValueError("License plate must be a non-empty string.")
        bus = BusVehicle.getWithLicencePlate(licensePlate)
        if bus is None:
            raise ValueError(f"BusVehicle with license plate '{licensePlate}' does not exist.")

        # Validate route
        if not isinstance(route, int):
            raise ValueError("Route number must be an integer.")
        route_obj = Route.getWithNumber(route)
        if route_obj is None:
            raise ValueError(f"Route with number '{route}' does not exist.")

        # Validate date
        if not isinstance(_date, date):
            raise ValueError("Date must be a datetime.date object.")
        today = date.today()
        one_year_later = today + timedelta(days=365)
        if not (today <= _date <= one_year_later):
            raise ValueError("Assignment date must be within one year from today.")

        # Create and add assignment
        assignment = self.btms.addAssignment(_date, bus, route_obj)
        return assignment