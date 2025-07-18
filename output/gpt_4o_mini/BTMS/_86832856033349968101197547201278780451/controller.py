from datetime import date
from assets.BTMS.model.umple import *


class BTMSController:
    def __init__(self):
        self.btms = BTMS()

    def create_driver(self, drivername: str):
        # Create a new driver and add it to the BTMS
        new_driver = self.btms.addDriver(drivername)
        return new_driver

    def create_route(self, number: int):
        # Create a new route and add it to the BTMS
        new_route = self.btms.addRoute(number)
        return new_route

    def create_route_assignment(self, licensePlate: str, route: int, _date: date):
        # Find the vehicle by license plate
        vehicle = BusVehicle.getWithLicencePlate(licensePlate)
        if vehicle is None:
            raise ValueError(f"No vehicle found with license plate: {licensePlate}")

        # Find the route by route number
        route_obj = Route.getWithNumber(route)
        if route_obj is None:
            raise ValueError(f"No route found with number: {route}")

        # Create a new route assignment and add it to the BTMS
        new_assignment = self.btms.addAssignment(_date, vehicle, route_obj)
        return new_assignment