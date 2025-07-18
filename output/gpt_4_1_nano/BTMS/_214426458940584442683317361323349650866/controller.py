from datetime import date
from assets.BTMS.model.ecore import *


class BTMSController:
    def __init__(self):
        self.btms = BTMS()

    def create_driver(self, drivername: str):
        # Create a new driver with the given name
        self.btms.create_driver(drivername)

    def create_route(self, number: int):
        # Create a new route with the specified number
        self.btms.create_route(number)

    def create_route_assignment(self, licensePlate: str, route: int, _date: date):
        # Create a new route assignment with the given vehicle license, route number, and date
        self.btms.create_route_assignment(licensePlate, route, _date)