from datetime import date
from assets.BTMS.model.umple import *


class BTMSController:
    def __init__(self):
        self.btms = BTMS()

    def create_driver(self, drivername: str):
        if not drivername:
            raise ValueError("The name of a driver cannot be empty.")
        try:
            return self.btms.addDriver(drivername)
        except RuntimeError as e:
            if "duplicate name" in str(e):
                raise ValueError("A driver with this name already exists.")
            raise

    def create_route(self, number: int):
        if number <= 0:
            raise ValueError("The number of a route must be greater than zero.")
        if number > 9999:
            raise ValueError("The number of a route cannot be greater than 9999.")
        try:
            return self.btms.addRoute(number)
        except RuntimeError as e:
            if "duplicate number" in str(e):
                raise ValueError("A route with this number already exists. Please use a different number.")
            raise

    def create_route_assignment(self, licensePlate: str, route: int, _date: date):
        # Validate bus exists
        bus = BusVehicle.getWithLicencePlate(licensePlate)
        if not bus:
            raise ValueError("A bus must be specified for the assignment.")
        
        # Validate route exists
        route_obj = Route.getWithNumber(route)
        if not route_obj:
            raise ValueError("A route must be specified for the assignment.")
        
        # Validate date is within one year from today
        today = date.today()
        one_year_later = date(today.year + 1, today.month, today.day)
        if _date < today or _date > one_year_later:
            raise ValueError("The date must be within a year from today.")
        
        try:
            return self.btms.addAssignment(_date, bus, route_obj)
        except Exception as e:
            raise ValueError(str(e))