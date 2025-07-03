from datetime import date
from assets.BTMS.model.umple import *

class BTMSController:
    def __init__(self):
        self.btms = BTMS()

    def create_driver(self, drivername: str):
        """
        Creates a new Driver with the given name and adds it to the BTMS.
        Raises RuntimeError if a driver with the same name already exists.
        Returns the created Driver instance.
        """
        if Driver.hasWithName(drivername):
            raise RuntimeError(f"Driver with name '{drivername}' already exists.")
        driver = self.btms.addDriver(drivername)
        return driver

    def create_route(self, number: int):
        """
        Creates a new Route with the given number and adds it to the BTMS.
        Raises RuntimeError if a route with the same number already exists.
        Returns the created Route instance.
        """
        if Route.hasWithNumber(number):
            raise RuntimeError(f"Route with number '{number}' already exists.")
        route = self.btms.addRoute(number)
        return route

    def create_route_assignment(self, licensePlate: str, route: int, _date: date):
        """
        Creates a new RouteAssignment for the given bus (by licensePlate), route (by number), and date.
        Raises RuntimeError if the bus or route does not exist.
        Returns the created RouteAssignment instance.
        """
        bus = BusVehicle.getWithLicencePlate(licensePlate)
        if bus is None:
            raise RuntimeError(f"Bus with license plate '{licensePlate}' does not exist.")
        route_obj = Route.getWithNumber(route)
        if route_obj is None:
            raise RuntimeError(f"Route with number '{route}' does not exist.")
        assignment = self.btms.addAssignment(_date, bus, route_obj)
        return assignment