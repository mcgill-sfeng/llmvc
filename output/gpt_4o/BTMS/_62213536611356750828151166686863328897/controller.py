from datetime import date, timedelta
from assets.BTMS.model.umple import *

class BTMSController:
    def __init__(self):
        self.btms = BTMS()

    def create_driver(self, drivername: str):
        # Check if the driver name is not empty
        if not drivername:
            raise ValueError("Driver name cannot be empty.")
        
        # Create a new driver in the BTMS system
        try:
            self.btms.add_driver(drivername)
        except Exception as e:
            raise RuntimeError(f"Failed to create driver: {str(e)}")

    def create_route(self, number: int):
        # Check if the route number is within the valid range
        if not (1 <= number <= 9999):
            raise ValueError("Route number must be between 1 and 9999.")
        
        # Create a new route in the BTMS system
        try:
            self.btms.add_route(number)
        except Exception as e:
            raise RuntimeError(f"Failed to create route: {str(e)}")

    def create_route_assignment(self, licensePlate: str, route: int, _date: date):
        # Check if the license plate is not empty
        if not licensePlate:
            raise ValueError("License plate cannot be empty.")
        
        # Check if the route number is within the valid range
        if not (1 <= route <= 9999):
            raise ValueError("Route number must be between 1 and 9999.")
        
        # Check if the date is within one year from today
        today = date.today()
        one_year_from_today = today + timedelta(days=365)
        if not (today <= _date <= one_year_from_today):
            raise ValueError("Date must be within one year from today.")
        
        # Create a new route assignment in the BTMS system
        try:
            self.btms.add_route_assignment(licensePlate, route, _date)
        except Exception as e:
            raise RuntimeError(f"Failed to create route assignment: {str(e)}")