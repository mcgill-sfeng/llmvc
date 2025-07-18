from datetime import date, timedelta
from assets.BTMS.model.umple import *

class BTMSController:
    def __init__(self):
        self.btms = BTMS()

    def create_driver(self, drivername: str):
        if not drivername or not isinstance(drivername, str):
            raise ValueError("Driver name must be a non-empty string.")
        
        # Assuming the BTMS model has a method to add a driver
        driver_id = self.btms.add_driver(drivername)
        return driver_id

    def create_route(self, number: int):
        if not isinstance(number, int) or not (1 <= number <= 9999):
            raise ValueError("Route number must be an integer between 1 and 9999.")
        
        # Assuming the BTMS model has a method to add a route
        route_id = self.btms.add_route(number)
        return route_id

    def create_route_assignment(self, licensePlate: str, route: int, _date: date):
        if not licensePlate or not isinstance(licensePlate, str):
            raise ValueError("License plate must be a non-empty string.")
        
        if not isinstance(route, int) or not (1 <= route <= 9999):
            raise ValueError("Route number must be an integer between 1 and 9999.")
        
        if not isinstance(_date, date):
            raise ValueError("Date must be a valid date object.")
        
        today = date.today()
        if not (today <= _date <= today + timedelta(days=365)):
            raise ValueError("Date must be within one year from today.")

        # Assuming the BTMS model has a method to create a route assignment
        assignment_id = self.btms.create_route_assignment(licensePlate, route, _date)
        return assignment_id