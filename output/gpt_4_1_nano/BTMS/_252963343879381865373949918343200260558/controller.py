from datetime import date
from assets.BTMS.model.ecore import *

class BTMSController:
    def __init__(self):
        self.btms = BTMS()

    def create_driver(self, drivername: str):
        # Create a new Driver instance with the given name
        driver = Driver(name=drivername)
        # Add the driver to the BTMS's collection of drivers
        self.btms.drivers.append(driver)

    def create_route(self, number: int):
        # Create a new Route instance with the given number
        route = Route(number=number)
        # Add the route to the BTMS's collection of routes
        self.btms.routes.append(route)

    def create_route_assignment(self, licensePlate: str, route: int, _date: date):
        # Find the BusVehicle with the specified licensePlate
        vehicle = None
        for v in self.btms.vehicles:
            if v.licencePlate == licensePlate:
                vehicle = v
                break
        if vehicle is None:
            # If vehicle not found, create a new one and add to the collection
            vehicle = BusVehicle(licencePlate=licensePlate)
            self.btms.vehicles.append(vehicle)

        # Find the Route with the specified number
        route_obj = None
        for r in self.btms.routes:
            if r.number == route:
                route_obj = r
                break
        if route_obj is None:
            # If route not found, create a new one and add to the collection
            route_obj = Route(number=route)
            self.btms.routes.append(route_obj)

        # Create a new RouteAssignment with the specified date, bus, and route
        assignment = RouteAssignment(date=_date, bus=vehicle, route=route_obj)

        # Add the assignment to the BTMS's collection
        self.btms.assignments.append(assignment)

        # Link the assignment to the vehicle's assignments
        if vehicle.assignments is None:
            vehicle.assignments = []
        vehicle.assignments.append(assignment)

        # Link the assignment to the route's assignments
        if route_obj.assignments is None:
            route_obj.assignments = []
        route_obj.assignments.append(assignment)