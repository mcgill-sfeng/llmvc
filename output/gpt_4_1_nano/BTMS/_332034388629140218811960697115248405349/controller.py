from datetime import date
from assets.BTMS.model.umple import *


class BTMSController:
    def __init__(self):
        self.btms = BTMS()

    def create_driver(self, drivername: str):
        """
        Creates a new Driver with the given name and adds it to the BTMS.
        """
        # Use the addDriver1 method to create and add a Driver
        self.btms.addDriver1(drivername)

    def create_route(self, number: int):
        """
        Creates a new Route with the given number and adds it to the BTMS.
        """
        # Use the addRoute1 method to create and add a Route
        self.btms.addRoute1(number)

    def create_route_assignment(self, licensePlate: str, route: int, _date: date):
        """
        Creates a new RouteAssignment with the specified bus license plate, route number, and date,
        then adds it to the BTMS.
        """
        # Retrieve the vehicle (bus) with the given license plate
        vehicle = None
        for v in self.btms.getVehicles():
            if v.getLicencePlate() == licensePlate:
                vehicle = v
                break
        if vehicle is None:
            # If vehicle not found, create and add it
            self.btms.addVehicle1(licensePlate)
            # Retrieve again after creation
            for v in self.btms.getVehicles():
                if v.getLicencePlate() == licensePlate:
                    vehicle = v
                    break

        # Retrieve the route with the given number
        route_obj = None
        for r in self.btms.getRoutes():
            if r.getNumber() == route:
                route_obj = r
                break
        if route_obj is None:
            # If route not found, create and add it
            self.btms.addRoute1(route)
            for r in self.btms.getRoutes():
                if r.getNumber() == route:
                    route_obj = r
                    break

        # Create the RouteAssignment
        self.btms.addAssignment1(_date, vehicle, route_obj)