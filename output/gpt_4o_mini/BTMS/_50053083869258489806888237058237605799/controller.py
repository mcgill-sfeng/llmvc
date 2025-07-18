from datetime import date
from assets.BTMS.model.ecore import *

class BTMSController:
    def __init__(self):
        self.btms = BTMS()

    def create_driver(self, drivername: str):
        # Create a new Driver instance
        new_driver = Driver(name=drivername)
        # Add the new driver to the BTMS drivers list
        self.btms.drivers.append(new_driver)

    def create_route(self, number: int):
        # Create a new Route instance
        new_route = Route(number=number)
        # Add the new route to the BTMS routes list
        self.btms.routes.append(new_route)

    def create_route_assignment(self, licensePlate: str, route: int, _date: date):
        # Find the bus vehicle by license plate
        bus_vehicle = next((vehicle for vehicle in self.btms.vehicles if vehicle.licencePlate == licensePlate), None)
        # Find the route by number
        route_instance = next((r for r in self.btms.routes if r.number == route), None)

        if bus_vehicle is None:
            raise ValueError(f"No bus vehicle found with license plate: {licensePlate}")
        if route_instance is None:
            raise ValueError(f"No route found with number: {route}")

        # Create a new RouteAssignment instance
        new_assignment = RouteAssignment(date=_date, bus=bus_vehicle, route=route_instance)
        # Add the new assignment to the BTMS assignments list
        self.btms.assignments.append(new_assignment)
        # Also add the assignment to the bus vehicle and route
        bus_vehicle.assignments.append(new_assignment)
        route_instance.assignments.append(new_assignment)