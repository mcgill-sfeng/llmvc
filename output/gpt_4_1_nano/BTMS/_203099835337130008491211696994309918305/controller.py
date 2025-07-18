from datetime import date
from assets.BTMS.model.umple import *

class BTMSController:
    def __init__(self):
        self.btms = BTMS()

    def create_driver(self, drivername: str):
        # Creates a new Driver with the given name and adds it to the BTMS
        return self.btms.addDriver(drivername)

    def create_route(self, number: int):
        # Creates a new Route with the given number and adds it to the BTMS
        return self.btms.addRoute(number)

    def create_route_assignment(self, licensePlate: str, route: int, _date: date):
        # Creates a new RouteAssignment with the specified date, bus, and route
        # First, retrieve the BusVehicle by licensePlate
        bus = self.btms.getVehicle(self.btms.indexOfVehicle(self.btms.getVehicle(0))) if self.btms.hasVehicles() else None
        # Since getVehicle requires an index, find the vehicle with matching licensePlate
        bus = None
        for v in self.btms.getVehicles():
            if v.getLicencePlate() == licensePlate:
                bus = v
                break
        if bus is None:
            # If bus with licensePlate doesn't exist, create it
            bus = self.btms.addVehicle(licensePlate)
        # Retrieve the Route by number
        route_obj = None
        for r in self.btms.getRoutes():
            if r.getNumber() == route:
                route_obj = r
                break
        if route_obj is None:
            # If route doesn't exist, create it
            route_obj = self.btms.addRoute(route)
        # Create the RouteAssignment
        return self.btms.addAssignment(_date, bus, route_obj)