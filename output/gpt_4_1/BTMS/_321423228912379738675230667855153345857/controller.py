from datetime import date
from assets.BTMS.model.umple import *

class BTMSController:
    def __init__(self):
        self.btms = BTMS()

    def create_driver(self, drivername: str):
        # Check uniqueness: no driver with this name should exist
        if Driver.hasWithName(drivername):
            raise ValueError(f"Driver with name '{drivername}' already exists.")
        # Create and add the driver
        driver = Driver(drivername, self.btms)
        self.btms.addDriver2(driver)
        return driver

    def create_route(self, number: int):
        # Check uniqueness: no route with this number should exist
        if Route.hasWithNumber(number):
            raise ValueError(f"Route with number '{number}' already exists.")
        # Create and add the route
        route = Route(number, self.btms)
        self.btms.addRoute2(route)
        return route

    def create_route_assignment(self, licensePlate: str, route: int, _date: date):
        # Find the BusVehicle by licensePlate
        if not BusVehicle.hasWithLicencePlate(licensePlate):
            raise ValueError(f"BusVehicle with license plate '{licensePlate}' does not exist.")
        bus = BusVehicle.getWithLicencePlate(licensePlate)

        # Find the Route by number
        if not Route.hasWithNumber(route):
            raise ValueError(f"Route with number '{route}' does not exist.")
        route_obj = Route.getWithNumber(route)

        # Check for duplicate assignment (same bus, route, and date)
        for assignment in self.btms.getAssignments():
            if (assignment.getBus() == bus and
                assignment.getRoute() == route_obj and
                assignment.getDate() == _date):
                raise ValueError("RouteAssignment for this bus, route, and date already exists.")

        # Create and add the assignment
        assignment = RouteAssignment(_date, bus, route_obj, self.btms)
        self.btms.addAssignment2(assignment)
        return assignment