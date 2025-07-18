from datetime import date
from assets.BTMS.model.ecore import *

class BTMSController:
    def __init__(self):
        self.btms = BTMS()

    def create_driver(self, drivername: str):
        # Check if driver already exists (by name)
        for driver in self.btms.drivers:
            if driver.name == drivername:
                return driver  # Optionally, raise an exception or return None
        # Create new driver
        new_driver = Driver(name=drivername, schedules=[])
        self.btms.drivers.append(new_driver)
        return new_driver

    def create_route(self, number: int):
        # Check if route already exists (by number)
        for route in self.btms.routes:
            if route.number == number:
                return route  # Optionally, raise an exception or return None
        # Create new route
        new_route = Route(number=number, assignments=[])
        self.btms.routes.append(new_route)
        return new_route

    def create_route_assignment(self, licensePlate: str, route: int, _date: date):
        # Find the bus by license plate
        bus = None
        for v in self.btms.vehicles:
            if v.licencePlate == licensePlate:
                bus = v
                break
        if bus is None:
            raise ValueError(f"Bus with license plate {licensePlate} not found.")

        # Find the route by number
        route_obj = None
        for r in self.btms.routes:
            if r.number == route:
                route_obj = r
                break
        if route_obj is None:
            raise ValueError(f"Route with number {route} not found.")

        # Create the route assignment
        assignment = RouteAssignment(date=_date, bus=bus, route=route_obj, schedules=[])
        # Add assignment to bus and route
        bus.assignments.append(assignment)
        route_obj.assignments.append(assignment)
        self.btms.assignments.append(assignment)
        return assignment