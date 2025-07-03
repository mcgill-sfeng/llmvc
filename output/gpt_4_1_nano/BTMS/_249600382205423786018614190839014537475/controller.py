from datetime import date
from assets.BTMS.model.umple import *

class BTMSController:
    def __init__(self):
        self.btms = BTMS()

    def create_driver(self, drivername: str):
        # Creates a new Driver with the given name and adds to BTMS
        return self.btms.addDriver(drivername)

    def create_route(self, number: int):
        # Creates a new Route with the given number and adds to BTMS
        return self.btms.addRoute(number)

    def create_route_assignment(self, licensePlate: str, route: int, _date: date):
        # Validate date: must be within one year from today
        today = date.today()
        delta_days = abs((_date - today).days)
        if delta_days > 365:
            raise ValueError("Date must be within one year from today.")
        # Retrieve BusVehicle by licensePlate
        bus = self.btms.getVehicle(self.btms.getVehicle, licensePlate)
        if bus is None:
            # If not exists, create new BusVehicle
            bus = self.btms.addVehicle(licensePlate)
        # Retrieve Route by route number
        route_obj = self.btms.getRoute(self.btms.getRoute, route)
        if route_obj is None:
            # If not exists, create new Route
            route_obj = self.btms.addRoute(route)
        # Create RouteAssignment
        assignment = self.btms.addAssignment(_date, bus, route_obj)
        return assignment