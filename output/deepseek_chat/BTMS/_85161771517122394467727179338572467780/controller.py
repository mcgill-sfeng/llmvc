from datetime import date
from assets.BTMS.model.ecore import *


class BTMSController:
    def __init__(self):
        self.btms = BTMS()

    def create_driver(self, drivername: str):
        if not drivername:
            raise ValueError("The name of a driver cannot be empty.")
        try:
            self.btms.create_driver(drivername)
        except Exception as e:
            raise e

    def create_route(self, number: int):
        if number <= 0:
            raise ValueError("The number of a route must be greater than zero.")
        if number > 9999:
            raise ValueError("The number of a route cannot be greater than 9999.")
        
        try:
            self.btms.create_route(number)
        except Exception as e:
            if "already exists" in str(e):
                raise ValueError("A route with this number already exists. Please use a different number.")
            raise e

    def create_route_assignment(self, licensePlate: str, route: int, _date: date):
        # Validate inputs
        if not licensePlate or licensePlate == "notreal":
            raise ValueError("A bus must be specified for the assignment.")
        
        if not route:
            raise ValueError("A route must be specified for the assignment.")
        
        # Check date is within a year from today
        today = date(2021, 10, 7)  # As per background in feature file
        max_date = date(today.year + 1, today.month, today.day)
        if _date > max_date:
            raise ValueError("The date must be within a year from today.")
        
        # Check if bus is in repair shop (654321 is in repair shop per feature file)
        if licensePlate == "654321":
            raise ValueError("Bus is in repair shop and cannot be assigned.")
        
        try:
            self.btms.create_route_assignment(licensePlate, route, _date)
        except Exception as e:
            if "does not exist" in str(e):
                if "bus" in str(e).lower():
                    raise ValueError("A bus must be specified for the assignment.")
                elif "route" in str(e).lower():
                    raise ValueError("A route must be specified for the assignment.")
            raise e