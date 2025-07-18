from datetime import date
from assets.BTMS.model.umple import *


class BTMSController:
    def __init__(self):
        self.btms = BTMS()

    def create_driver(self, drivername: str):
        if not drivername:
            raise ValueError("The name of a driver cannot be empty.")
        self.btms.create_driver(drivername)

    def create_route(self, number: int):
        if number <= 0:
            raise ValueError("The number of a route must be greater than zero.")
        if number > 9999:
            raise ValueError("The number of a route cannot be greater than 9999.")
        
        # Check if route already exists (assuming BTMS has a method to check this)
        if hasattr(self.btms, 'route_exists') and self.btms.route_exists(number):
            raise ValueError("A route with this number already exists. Please use a different number.")
            
        self.btms.create_route(number)

    def create_route_assignment(self, licensePlate: str, route: int, _date: date):
        # Validate bus exists and not in repair shop
        if not licensePlate or not self.btms.bus_exists(licensePlate):
            raise ValueError("A bus must be specified for the assignment.")
        
        if self.btms.bus_in_repair(licensePlate):
            raise ValueError("Cannot assign a bus that's in the repair shop.")
        
        # Validate route exists
        if not route or not self.btms.route_exists(route):
            raise ValueError("A route must be specified for the assignment.")
        
        # Validate date is within a year from today
        today = date.today()
        one_year_later = date(today.year + 1, today.month, today.day)
        
        if _date < today or _date > one_year_later:
            raise ValueError("The date must be within a year from today.")
        
        # Check for existing assignment conflicts would go here if needed
        
        self.btms.create_route_assignment(licensePlate, route, _date)