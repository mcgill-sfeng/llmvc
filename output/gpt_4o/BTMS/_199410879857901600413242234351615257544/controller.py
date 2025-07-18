from datetime import date
from assets.BTMS.model.ecore import *

class BTMSController:
    def __init__(self):
        self.btms = BTMS()

    def create_driver(self, drivername: str):
        # Assuming BTMS has a method to add a driver
        # and it automatically generates a unique ID for the driver.
        if not drivername:
            raise ValueError("Driver name cannot be empty.")
        
        try:
            self.btms.add_driver(drivername)
        except Exception as e:
            # Handle exceptions that might occur during driver creation
            print(f"Error creating driver: {e}")

    def create_route(self, number: int):
        # Assuming BTMS has a method to add a route
        if not (1 <= number <= 9999):
            raise ValueError("Route number must be between 1 and 9999.")
        
        try:
            self.btms.add_route(number)
        except Exception as e:
            # Handle exceptions that might occur during route creation
            print(f"Error creating route: {e}")

    def create_route_assignment(self, licensePlate: str, route: int, _date: date):
        # Assuming BTMS has a method to add a route assignment
        if not licensePlate:
            raise ValueError("License plate cannot be empty.")
        
        if not (1 <= route <= 9999):
            raise ValueError("Route number must be between 1 and 9999.")
        
        if not isinstance(_date, date):
            raise ValueError("Invalid date format.")
        
        today = date.today()
        one_year_from_today = date(today.year + 1, today.month, today.day)
        
        if not (today <= _date < one_year_from_today):
            raise ValueError("Date must be within one year from today.")
        
        try:
            self.btms.add_route_assignment(licensePlate, route, _date)
        except Exception as e:
            # Handle exceptions that might occur during route assignment creation
            print(f"Error creating route assignment: {e}")