from datetime import date
from assets.BTMS.model.umple import *

class BTMSController:
    def __init__(self):
        self.btms = BTMS()

    def create_driver(self, drivername: str):
        """
        Creates a new Driver with the given name and adds it to the BTMS.
        """
        # Use the addDriver1 method to create and add a new Driver
        self.btms.addDriver1(drivername)

    def create_route(self, number: int):
        """
        Creates a new Route with the given number and adds it to the BTMS.
        """
        # Use the addRoute1 method to create and add a new Route
        self.btms.addRoute1(number)

    def create_route_assignment(self, licensePlate: str, route: int, _date: date):
        """
        Creates a new RouteAssignment with the specified bus (by licensePlate),
        route number, and date, then adds it to the BTMS.
        """
        # Retrieve the BusVehicle by licensePlate
        bus = None
        for i in range(self.btms.numberOfVehicles()):
            vehicle = self.btms.getVehicle(i)
            if vehicle.getLicencePlate() == licensePlate:
                bus = vehicle
                break
        if bus is None:
            # If the bus does not exist, create and add it
            self.btms.addVehicle1(licensePlate)
            bus = self.btms.getVehicle(self.btms.numberOfVehicles() - 1)

        # Retrieve the Route by number
        route_obj = None
        for i in range(self.btms.numberOfRoutes()):
            r = self.btms.getRoute(i)
            if r.getNumber() == route:
                route_obj = r
                break
        if route_obj is None:
            # If the route does not exist, create and add it
            self.btms.addRoute1(route)
            route_obj = self.btms.getRoute(self.btms.numberOfRoutes() - 1)

        # Create the RouteAssignment
        self.btms.addAssignment1(_date, bus, route_obj)