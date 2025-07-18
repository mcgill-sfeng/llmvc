from datetime import date
from assets.BTMS.model.ecore import *

class BTMSController:
    def __init__(self):
        self.btms = BTMS()

    def create_driver(self, drivername: str):
        # Create a new Driver instance
        new_driver = Driver(name=drivername)
        # Add the new driver to the BTMS drivers collection
        self.btms.drivers.append(new_driver)

    def create_route(self, number: int):
        # Create a new Route instance
        new_route = Route(number=number)
        # Add the new route to the BTMS routes collection
        self.btms.routes.append(new_route)

    def create_route_assignment(self, licensePlate: str, route: int, _date: date):
        # Find the bus with the given license plate
        bus = next((vehicle for vehicle in self.btms.vehicles if vehicle.licencePlate == licensePlate), None)
        if not bus:
            raise ValueError(f"No bus found with license plate: {licensePlate}")

        # Find the route with the given number
        route_obj = next((r for r in self.btms.routes if r.number == route), None)
        if not route_obj:
            raise ValueError(f"No route found with number: {route}")

        # Create a new RouteAssignment instance
        new_assignment = RouteAssignment(date=_date, bus=bus, route=route_obj)

        # Add the new assignment to the BTMS assignments collection
        self.btms.assignments.append(new_assignment)

        # Also, add the assignment to the bus and route's assignments
        bus.assignments.append(new_assignment)
        route_obj.assignments.append(new_assignment)