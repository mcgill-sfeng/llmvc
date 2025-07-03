from datetime import date
from assets.BTMS.model.umple import *

class BTMSController:
    def __init__(self):
        self.btms = BTMS()

    def create_driver(self, drivername: str):
        """
        Creates a new Driver with the given name and adds it to the BTMS.
        Returns the created Driver instance.
        """
        # Check if a driver with this name already exists (optional, for uniqueness)
        for i in range(self.btms.numberOfDrivers()):
            driver = self.btms.getDriver(i)
            if driver.getName() == drivername:
                return driver  # Already exists, return existing

        # Create and add new driver
        driver = self.btms.addDriver1(drivername)
        return driver

    def create_route(self, number: int):
        """
        Creates a new Route with the given number and adds it to the BTMS.
        Returns the created Route instance.
        """
        # Check if a route with this number already exists (optional, for uniqueness)
        for i in range(self.btms.numberOfRoutes()):
            route = self.btms.getRoute(i)
            if route.getNumber() == number:
                return route  # Already exists, return existing

        # Create and add new route
        route = self.btms.addRoute1(number)
        return route

    def create_route_assignment(self, licensePlate: str, route: int, _date: date):
        """
        Creates a new RouteAssignment for the given bus (by licensePlate), route (by number), and date.
        Returns the created RouteAssignment instance.
        """
        # Find the BusVehicle by licensePlate
        bus = None
        for i in range(self.btms.numberOfVehicles()):
            v = self.btms.getVehicle(i)
            if v.getLicencePlate() == licensePlate:
                bus = v
                break
        if bus is None:
            # If not found, create and add the bus
            bus = self.btms.addVehicle1(licensePlate)

        # Find the Route by number
        route_obj = None
        for i in range(self.btms.numberOfRoutes()):
            r = self.btms.getRoute(i)
            if r.getNumber() == route:
                route_obj = r
                break
        if route_obj is None:
            # If not found, create and add the route
            route_obj = self.btms.addRoute1(route)

        # Create and add the assignment
        assignment = self.btms.addAssignment1(_date, bus, route_obj)
        return assignment