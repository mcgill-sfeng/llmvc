from datetime import date
from assets.BTMS.model.umple import *

class BTMSController:
    def __init__(self):
        self.btms = BTMS()

    def create_driver(self, drivername: str):
        if not drivername:
            raise ValueError("The name of a driver cannot be empty.")
        
        new_driver = Driver(drivername, self.btms)
        self.btms.addDriver(new_driver)

    def create_route(self, number: int):
        if number <= 0:
            raise ValueError("The number of a route must be greater than zero.")
        if number > 9999:
            raise ValueError("The number of a route cannot be greater than 9999.")
        
        if Route.getWithNumber(number):
            raise ValueError("A route with this number already exists. Please use a different number.")
        
        new_route = Route(number, self.btms)
        self.btms.addRoute(new_route)

    def create_route_assignment(self, licensePlate: str, route: int, _date: date):
        if not licensePlate:
            raise ValueError("A bus must be specified for the assignment.")
        
        vehicle = BusVehicle.getWithLicencePlate(licensePlate)
        if vehicle is None:
            raise ValueError("A bus must be specified for the assignment.")
        
        if not self.btms.getRoute(route):
            raise ValueError("A route must be specified for the assignment.")
        
        if _date < date.today() or _date > date.today().replace(year=date.today().year + 1):
            raise ValueError("The date must be within a year from today.")
        
        new_assignment = RouteAssignment(_date, vehicle, self.btms.getRoute(route), self.btms)
        self.btms.addAssignment(new_assignment)