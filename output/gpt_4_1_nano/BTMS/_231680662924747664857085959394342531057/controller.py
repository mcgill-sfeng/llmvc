from datetime import date
from assets.BTMS.model.umple import *

class BTMSController:
    def __init__(self):
        self.btms = BTMS()

    def create_driver(self, drivername: str):
        # Create a new Driver object with the given name
        driver = Driver(name=drivername)
        # Add the driver to the BTMS's drivers collection
        self.btms.addDriver(driver)

    def create_route(self, number: int):
        # Create a new Route object with the given number
        route = Route(number=number)
        # Add the route to the BTMS's routes collection
        self.btms.addRoute(route)

    def create_route_assignment(self, licensePlate: str, route: int, _date: date):
        # Find the BusVehicle with the given licensePlate
        vehicle = None
        for v in self.btms.getVehicles():
            if v.licencePlate == licensePlate:
                vehicle = v
                break
        if vehicle is None:
            # If vehicle not found, create and add it
            vehicle = BusVehicle(licencePlate=licensePlate)
            self.btms.addVehicle(vehicle)

        # Find the Route with the given number
        route_obj = None
        for r in self.btms.getRoutes():
            if r.number == route:
                route_obj = r
                break
        if route_obj is None:
            # If route not found, create and add it
            route_obj = Route(number=route)
            self.btms.addRoute(route_obj)

        # Create a new RouteAssignment with the specified date
        assignment = RouteAssignment(date=_date)
        # Link the assignment to the vehicle and route
        assignment.setBus(vehicle)
        assignment.setRoute(route_obj)
        # Add the assignment to the BTMS's assignments collection
        self.btms.addAssignment(assignment)