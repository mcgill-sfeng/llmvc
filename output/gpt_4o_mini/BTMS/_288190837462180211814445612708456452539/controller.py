from datetime import date
from assets.BTMS.model.umple import *

class BTMSController:
    def __init__(self):
        self.btms = BTMS()

    def create_driver(self, drivername: str):
        # Create a new Driver instance
        new_driver = Driver(drivername, self.btms)
        # Add the new driver to the BTMS
        self.btms.addDriver(new_driver)

    def create_route(self, number: int):
        # Create a new Route instance
        new_route = Route(number, self.btms)
        # Add the new route to the BTMS
        self.btms.addRoute(new_route)

    def create_route_assignment(self, licensePlate: str, route: int, _date: date):
        # Find the vehicle with the given license plate
        vehicle = None
        for v in self.btms.getVehicles():
            if v.getLicencePlate() == licensePlate:
                vehicle = v
                break
        
        # Find the route with the given number
        route_obj = None
        for r in self.btms.getRoutes():
            if r.getNumber() == route:
                route_obj = r
                break
        
        # If both vehicle and route are found, create a RouteAssignment
        if vehicle and route_obj:
            new_assignment = RouteAssignment(_date, vehicle, route_obj, self.btms)
            # Add the new assignment to the BTMS
            self.btms.addAssignment(new_assignment)
        else:
            raise ValueError("Vehicle with license plate '{}' or route '{}' not found.".format(licensePlate, route))