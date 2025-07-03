from datetime import date, timedelta
from assets.BTMS.model.umple import *

class BTMSController:
    def __init__(self):
        self.btms = BTMS()

    def create_driver(self, drivername: str):
        # Check if the driver already exists
        if Driver.getWithName(drivername):
            raise ValueError("Driver with this name already exists.")
        
        # Create a new Driver and add it to the BTMS
        new_driver = Driver(drivername, self.btms)
        self.btms.addDriver(new_driver)

    def create_route(self, number: int):
        # Check if the route already exists
        if Route.getWithNumber(number):
            raise ValueError("Route with this number already exists.")
        
        # Create a new Route and add it to the BTMS
        new_route = Route(number, self.btms)
        self.btms.addRoute(new_route)

    def create_route_assignment(self, licensePlate: str, route: int, _date: date):
        # Validate the date
        if _date < date.today() or _date > date.today() + timedelta(days=365):
            raise ValueError("Date must be within one year from today.")
        
        # Find the BusVehicle by license plate
        bus = BusVehicle.getWithLicencePlate(licensePlate)
        if bus is None:
            raise ValueError("Bus with this license plate does not exist.")
        
        # Find the Route by number
        route_obj = Route.getWithNumber(route)
        if route_obj is None:
            raise ValueError("Route with this number does not exist.")
        
        # Create a new RouteAssignment and add it to the BTMS
        new_assignment = RouteAssignment(_date, bus, route_obj, self.btms)
        self.btms.addAssignment(new_assignment)