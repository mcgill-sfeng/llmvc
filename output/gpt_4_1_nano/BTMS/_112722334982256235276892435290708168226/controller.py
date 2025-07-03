from datetime import date
from assets.BTMS.model.umple import *

class BTMSController:
    def __init__(self):
        self.btms = BTMS()

    def create_driver(self, drivername: str):
        # Create a new Driver with the given name and add to BTMS
        self.btms.addDriver(drivername)

    def create_route(self, number: int):
        # Create a new Route with the given number and add to BTMS
        self.btms.addRoute(number)

    def create_route_assignment(self, licensePlate: str, route: int, _date: date):
        # Validate date: must be within one year from today
        today = date.today()
        delta_days = abs((_date - today).days)
        if delta_days > 365:
            raise ValueError("Date must be within one year from today.")
        # Retrieve the BusVehicle by licensePlate
        vehicle = None
        for v in self.btms.getVehicles():
            if v.getLicencePlate() == licensePlate:
                vehicle = v
                break
        if vehicle is None:
            raise ValueError(f"BusVehicle with license plate '{licensePlate}' not found.")
        # Retrieve the Route by number
        route_obj = None
        for r in self.btms.getRoutes():
            if r.getNumber() == route:
                route_obj = r
                break
        if route_obj is None:
            raise ValueError(f"Route with number '{route}' not found.")
        # Create the RouteAssignment
        self.btms.addAssignment(_date, vehicle, route_obj)