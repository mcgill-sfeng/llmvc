from datetime import date
from assets.BTMS.model.umple import *

class BTMSController:
    def __init__(self):
        self.btms = BTMS()

    def create_driver(self, drivername: str):
        # Check if driver already exists
        for driver in self.btms.getDrivers():
            if driver.getName() == drivername:
                raise ValueError(f"Driver with name '{drivername}' already exists.")
        # Create and add new driver
        self.btms.addDriver(drivername)

    def create_route(self, number: int):
        # Check if route already exists
        for route in self.btms.getRoutes():
            if route.getNumber() == number:
                raise ValueError(f"Route with number '{number}' already exists.")
        # Create and add new route
        self.btms.addRoute(number)

    def create_route_assignment(self, licensePlate: str, route: int, _date: date):
        # Find the bus vehicle by license plate
        bus = None
        for v in self.btms.getVehicles():
            if v.getLicencePlate() == licensePlate:
                bus = v
                break
        if bus is None:
            raise ValueError(f"BusVehicle with licencePlate '{licensePlate}' not found.")

        # Find the route by number
        route_obj = None
        for r in self.btms.getRoutes():
            if r.getNumber() == route:
                route_obj = r
                break
        if route_obj is None:
            raise ValueError(f"Route with number '{route}' not found.")

        # Check if assignment for this bus, route, and date already exists
        for assignment in self.btms.getAssignments():
            if (assignment.getBus() == bus and
                assignment.getRoute() == route_obj and
                assignment.getDate() == _date):
                raise ValueError("RouteAssignment for this bus, route, and date already exists.")

        # Create and add new route assignment
        self.btms.addAssignment(_date, bus, route_obj)