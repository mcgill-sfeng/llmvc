from datetime import date, timedelta
from assets.BTMS.model.umple import *

class BTMSController:
    def __init__(self):
        self.btms = BTMS()

    def create_driver(self, drivername: str):
        if not drivername:
            raise ValueError("The name of a driver cannot be empty.")
        
        # Create a new driver and add to BTMS
        new_driver = Driver(drivername, self.btms)
        self.btms.addDriver(new_driver)

    def create_route(self, number: int):
        if number <= 0:
            raise ValueError("The number of a route must be greater than zero.")
        if number > 9999:
            raise ValueError("The number of a route cannot be greater than 9999.")
        if Route.getWithNumber(number):
            raise ValueError("A route with this number already exists. Please use a different number.")
        
        # Create a new route and add to BTMS
        new_route = Route(number, self.btms)
        self.btms.addRoute(new_route)

    def create_route_assignment(self, licensePlate: str, route: int, _date: date):
        # Validate the date
        if _date < date.today() or _date > date.today() + timedelta(days=365):
            raise ValueError("The date must be within a year from today.")
        
        # Validate the bus vehicle
        bus = BusVehicle.getWithLicencePlate(licensePlate)
        if bus is None:
            raise ValueError("A bus must be specified for the assignment.")
        
        # Validate the route
        route_obj = Route.getWithNumber(route)
        if route_obj is None:
            raise ValueError("A route must be specified for the assignment.")
        
        # Create a new route assignment and add to BTMS
        new_assignment = RouteAssignment(_date, bus, route_obj, self.btms)
        self.btms.addAssignment(new_assignment)