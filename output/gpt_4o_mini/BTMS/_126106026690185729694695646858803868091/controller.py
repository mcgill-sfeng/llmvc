from datetime import date, timedelta
from assets.BTMS.model.umple import *

class BTMSController:
    def __init__(self):
        self.btms = BTMS()

    def create_driver(self, drivername: str):
        if not drivername:
            raise ValueError("Driver name cannot be empty.")
        
        # Check if the driver already exists
        if Driver.getWithName(drivername):
            raise ValueError("Driver with this name already exists.")
        
        # Create and add the new driver
        new_driver = Driver(drivername, self.btms)
        self.btms.addDriver(new_driver)

    def create_route(self, number: int):
        if number < 1 or number > 9999:
            raise ValueError("Route number must be between 1 and 9999.")
        
        # Check if the route already exists
        if Route.getWithNumber(number):
            raise ValueError("Route with this number already exists.")
        
        # Create and add the new route
        new_route = Route(number, self.btms)
        self.btms.addRoute(new_route)

    def create_route_assignment(self, licensePlate: str, route: int, _date: date):
        if not licensePlate:
            raise ValueError("License plate cannot be empty.")
        
        if not (1 <= route <= 9999):
            raise ValueError("Route number must be between 1 and 9999.")
        
        if _date < date.today() or _date > date.today() + timedelta(days=365):
            raise ValueError("Date must be within one year from today.")
        
        # Find the bus vehicle and route
        bus = BusVehicle.getWithLicencePlate(licensePlate)
        route_obj = Route.getWithNumber(route)
        
        if bus is None:
            raise ValueError("Bus with this license plate does not exist.")
        
        if route_obj is None:
            raise ValueError("Route with this number does not exist.")
        
        # Create and add the new route assignment
        new_assignment = RouteAssignment(_date, bus, route_obj, self.btms)
        self.btms.addAssignment(new_assignment)