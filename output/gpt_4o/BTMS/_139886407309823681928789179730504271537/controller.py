from datetime import date
from assets.BTMS.model.umple import *
from assets.BTMS.model.umple import *

class BTMSController:
    def __init__(self):
        self.btms = BTMS()

    def create_driver(self, drivername: str):
        # Check if a driver with the same name already exists
        if Driver.hasWithName(drivername):
            raise ValueError(f"Driver with name '{drivername}' already exists.")
        # Add a new driver to the BTMS
        self.btms.addDriver(drivername)

    def create_route(self, number: int):
        # Check if a route with the same number already exists
        if Route.hasWithNumber(number):
            raise ValueError(f"Route with number '{number}' already exists.")
        # Add a new route to the BTMS
        self.btms.addRoute(number)

    def create_route_assignment(self, licensePlate: str, route: int, _date: date):
        # Retrieve the bus vehicle using the license plate
        bus = BusVehicle.getWithLicencePlate(licensePlate)
        if bus is None:
            raise ValueError(f"No bus found with license plate '{licensePlate}'.")

        # Retrieve the route using the route number
        route_obj = Route.getWithNumber(route)
        if route_obj is None:
            raise ValueError(f"No route found with number '{route}'.")

        # Create a new route assignment
        self.btms.addAssignment(_date, bus, route_obj)