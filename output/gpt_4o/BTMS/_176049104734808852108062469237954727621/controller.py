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
        # Find the vehicle with the given license plate
        vehicle = None
        for v in self.btms.getVehicles():
            if v.getLicencePlate() == licensePlate:
                vehicle = v
                break
        if vehicle is None:
            raise ValueError(f"No vehicle found with license plate {licensePlate}.")

        # Find the route with the given number
        route_obj = None
        for r in self.btms.getRoutes():
            if r.getNumber() == route:
                route_obj = r
                break
        if route_obj is None:
            raise ValueError(f"No route found with number {route}.")

        # Add a new route assignment to the BTMS
        self.btms.addAssignment1(_date, vehicle, route_obj)