from datetime import date, timedelta
from assets.BTMS.model.umple import *

class BTMSController:
    def __init__(self):
        self.btms = BTMS()

    def create_driver(self, drivername: str):
        if not drivername:
            raise ValueError("The name of a driver cannot be empty.")
        self.btms.add_driver(drivername)

    def create_route(self, number: int):
        if number <= 0:
            raise ValueError("The number of a route must be greater than zero.")
        if number > 9999:
            raise ValueError("The number of a route cannot be greater than 9999.")
        if self.btms.route_exists(number):
            raise ValueError("A route with this number already exists. Please use a different number.")
        self.btms.add_route(number)

    def create_route_assignment(self, licensePlate: str, route: int, _date: date):
        if not self.btms.bus_exists(licensePlate):
            raise ValueError("A bus must be specified for the assignment.")
        if not self.btms.route_exists(route):
            raise ValueError("A route must be specified for the assignment.")
        if self.btms.is_bus_in_repair(licensePlate):
            raise ValueError("The bus is currently in the repair shop and cannot be assigned.")
        current_date = date.today()
        if not (current_date <= _date <= current_date + timedelta(days=365)):
            raise ValueError("The date must be within a year from today.")
        self.btms.add_route_assignment(licensePlate, route, _date)