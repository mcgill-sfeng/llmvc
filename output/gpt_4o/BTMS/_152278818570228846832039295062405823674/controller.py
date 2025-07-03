from datetime import date
from assets.BTMS.model.umple import *

class BTMSController:
    def __init__(self):
        self.btms = BTMS()

    def create_driver(self, drivername: str):
        # Check if a driver with the same name already exists
        if Driver.hasWithName(drivername):
            raise ValueError(f"Driver with name {drivername} already exists.")
        
        # Add the driver to the BTMS
        self.btms.addDriver1(drivername)

    def create_route(self, number: int):
        # Check if a route with the same number already exists
        if Route.hasWithNumber(number):
            raise ValueError(f"Route with number {number} already exists.")
        
        # Add the route to the BTMS
        self.btms.addRoute1(number)

    def create_route_assignment(self, licensePlate: str, route: int, _date: date):
        # Validate the date
        today = date.today()
        if not (today <= _date <= today.replace(year=today.year + 1)):
            raise ValueError("Date must be within one year from today.")
        
        # Find the bus vehicle by license plate
        if not BusVehicle.hasWithLicencePlate(licensePlate):
            raise ValueError(f"No bus vehicle with license plate {licensePlate} found.")
        bus = BusVehicle.getWithLicencePlate(licensePlate)
        
        # Find the route by number
        if not Route.hasWithNumber(route):
            raise ValueError(f"No route with number {route} found.")
        route_obj = Route.getWithNumber(route)
        
        # Create the route assignment
        self.btms.addAssignment1(_date, bus, route_obj)