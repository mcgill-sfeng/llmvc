from datetime import date
from assets.BTMS.model.umple import *

class BTMSController:
    def __init__(self):
        self.btms = BTMS()

    def create_driver(self, drivername: str):
        # Check if the driver already exists
        if self.btms.hasDrivers() and Driver.getWithName(drivername):
            raise ValueError(f"Driver with name '{drivername}' already exists.")
        
        # Create a new driver and add it to the BTMS
        new_driver = Driver(drivername, self.btms)
        self.btms.addDriver2(new_driver)

    def create_route(self, number: int):
        # Check if the route already exists
        if self.btms.hasRoutes() and Route.getWithNumber(number):
            raise ValueError(f"Route with number '{number}' already exists.")
        
        # Create a new route and add it to the BTMS
        new_route = Route(number, self.btms)
        self.btms.addRoute2(new_route)

    def create_route_assignment(self, licensePlate: str, route: int, _date: date):
        # Find the bus vehicle by license plate
        if not self.btms.hasVehicles() or not BusVehicle.getWithLicencePlate(licensePlate):
            raise ValueError(f"No vehicle found with license plate '{licensePlate}'.")

        # Find the route by number
        if not self.btms.hasRoutes() or not Route.getWithNumber(route):
            raise ValueError(f"No route found with number '{route}'.")

        # Create a new route assignment and add it to the BTMS
        bus = BusVehicle.getWithLicencePlate(licensePlate)
        route_obj = Route.getWithNumber(route)
        new_assignment = RouteAssignment(_date, bus, route_obj, self.btms)
        self.btms.addAssignment2(new_assignment)