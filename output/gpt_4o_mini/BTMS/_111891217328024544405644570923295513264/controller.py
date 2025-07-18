from datetime import date
from assets.BTMS.model.umple import *

class BTMSController:
    def __init__(self):
        self.btms = BTMS()

    def create_driver(self, drivername: str):
        # Create a new Driver instance
        new_driver = Driver(name=drivername)
        # Add the new driver to the BTMS
        self.btms.drivers.add(new_driver)

    def create_route(self, number: int):
        # Create a new Route instance
        new_route = Route(number=number)
        # Add the new route to the BTMS
        self.btms.routes.add(new_route)

    def create_route_assignment(self, licensePlate: str, route: int, _date: date):
        # Find the bus vehicle by license plate
        bus_vehicle = next((vehicle for vehicle in self.btms.vehicles if vehicle.licencePlate == licensePlate), None)
        # Find the route by number
        route_instance = next((r for r in self.btms.routes if r.number == route), None)

        if bus_vehicle is None:
            raise ValueError(f"Bus vehicle with license plate {licensePlate} not found.")
        if route_instance is None:
            raise ValueError(f"Route with number {route} not found.")

        # Create a new RouteAssignment instance
        new_assignment = RouteAssignment(date=_date, bus=bus_vehicle, route=route_instance)
        # Add the new route assignment to the BTMS
        self.btms.assignments.add(new_assignment)