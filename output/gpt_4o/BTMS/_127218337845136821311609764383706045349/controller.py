from datetime import date, timedelta
from assets.BTMS.model.umple import *

class BTMSController:
    def __init__(self):
        self.btms = BTMS()

    def create_driver(self, drivername: str):
        if not drivername:
            raise ValueError("The name of a driver cannot be empty.")
        # Assuming BTMS has a method to add a driver
        self.btms.add_driver(drivername)

    def create_route(self, number: int):
        if number <= 0:
            raise ValueError("The number of a route must be greater than zero.")
        if number > 9999:
            raise ValueError("The number of a route cannot be greater than 9999.")
        # Assuming BTMS has a method to check if a route exists and to add a route
        if self.btms.route_exists(number):
            raise ValueError("A route with this number already exists. Please use a different number.")
        self.btms.add_route(number)

    def create_route_assignment(self, licensePlate: str, route: int, _date: date):
        # Assuming BTMS has methods to check if a bus and route exist
        if not self.btms.bus_exists(licensePlate):
            raise ValueError("A bus must be specified for the assignment.")
        if not self.btms.route_exists(route):
            raise ValueError("A route must be specified for the assignment.")
        
        # Check if the date is within one year from today
        today = date.today()
        one_year_from_today = today + timedelta(days=365)
        if not (today <= _date <= one_year_from_today):
            raise ValueError("The date must be within a year from today.")
        
        # Assuming BTMS has a method to add a route assignment
        self.btms.add_route_assignment(licensePlate, route, _date)