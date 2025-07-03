from datetime import date
from assets.BTMS.model.umple import *

class BTMSController:
    def __init__(self):
        self.btms = BTMS()

    def create_driver(self, drivername: str):
        # Check if a driver with the same name already exists
        if Driver.hasWithName(drivername):
            raise ValueError(f"Driver with name {drivername} already exists.")
        
        # Add a new driver to the BTMS
        self.btms.addDriver1(drivername)

    def create_route(self, number: int):
        # Check if a route with the same number already exists
        if Route.hasWithNumber(number):
            raise ValueError(f"Route with number {number} already exists.")
        
        # Add a new route to the BTMS
        self.btms.addRoute1(number)

    def create_route_assignment(self, licensePlate: str, route: int, _date: date):
        # Check if the vehicle with the given license plate exists
        if not BusVehicle.hasWithLicencePlate(licensePlate):
            raise ValueError(f"Bus with license plate {licensePlate} does not exist.")
        
        # Check if the route with the given number exists
        if not Route.hasWithNumber(route):
            raise ValueError(f"Route with number {route} does not exist.")
        
        # Retrieve the bus and route objects
        bus = BusVehicle.getWithLicencePlate(licensePlate)
        route_obj = Route.getWithNumber(route)
        
        # Add a new route assignment to the BTMS
        self.btms.addAssignment1(_date, bus, route_obj)