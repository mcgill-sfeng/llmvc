from datetime import date, timedelta
from assets.BTMS.model.umple import *


class BTMSController:
    def __init__(self):
        self.btms = BTMS()

    def create_driver(self, drivername: str):
        if not drivername:
            raise ValueError("The name of a driver cannot be empty.")
        # Assuming BTMS model has a method to add a driver
        self.btms.add_driver(drivername)

    def create_route(self, number: int):
        if number <= 0:
            raise ValueError("The number of a route must be greater than zero.")
        if number > 9999:
            raise ValueError("The number of a route cannot be greater than 9999.")
        
        # Assuming BTMS model has a method to check if route exists and add route
        if self.btms.route_exists(number):
            raise ValueError("A route with this number already exists. Please use a different number.")
        
        self.btms.add_route(number)

    def create_route_assignment(self, licensePlate: str, route: int, _date: date):
        # Validate bus vehicle exists and not in repair shop
        if not licensePlate or not self.btms.bus_exists(licensePlate):
            raise ValueError("A bus must be specified for the assignment.")
        
        if self.btms.bus_in_repair(licensePlate):
            raise ValueError("Cannot assign a bus that's in the repair shop.")
        
        # Validate route exists
        if not self.btms.route_exists(route):
            raise ValueError("A route must be specified for the assignment.")
        
        # Validate date is within one year from today
        today = date.today()
        one_year_later = today + timedelta(days=365)
        
        if _date < today or _date > one_year_later:
            raise ValueError("The date must be within a year from today.")
        
        # Check if assignment already exists for this bus on this date
        if self.btms.assignment_exists(licensePlate, _date):
            raise ValueError("This bus already has an assignment on this date.")
        
        # Create the assignment
        self.btms.add_route_assignment(licensePlate, route, _date)