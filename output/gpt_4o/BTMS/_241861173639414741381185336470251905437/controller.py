from datetime import date, timedelta
from assets.BTMS.model.umple import *

class BTMSController:
    def __init__(self):
        self.btms = BTMS()

    def create_driver(self, drivername: str):
        if not drivername:
            raise ValueError("The name of a driver cannot be empty.")
        self.btms.addDriver(drivername)

    def create_route(self, number: int):
        if number <= 0:
            raise ValueError("The number of a route must be greater than zero.")
        if number > 9999:
            raise ValueError("The number of a route cannot be greater than 9999.")
        if Route.hasWithNumber(number):
            raise ValueError("A route with this number already exists. Please use a different number.")
        self.btms.addRoute(number)

    def create_route_assignment(self, licensePlate: str, route: int, _date: date):
        if not BusVehicle.hasWithLicencePlate(licensePlate):
            raise ValueError("A bus must be specified for the assignment.")
        if not Route.hasWithNumber(route):
            raise ValueError("A route must be specified for the assignment.")
        
        current_date = date.today()
        if not (current_date <= _date <= current_date + timedelta(days=365)):
            raise ValueError("The date must be within a year from today.")
        
        bus = BusVehicle.getWithLicencePlate(licensePlate)
        route_obj = Route.getWithNumber(route)
        self.btms.addAssignment(_date, bus, route_obj)