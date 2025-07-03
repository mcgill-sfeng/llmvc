from datetime import date
from assets.BTMS.model.ecore import *

class BTMSController:
    def __init__(self):
        self.btms = BTMS()

    def create_driver(self, drivername: str):
        # Check if a driver with the same name already exists
        for driver in self.btms.drivers:
            if driver.name == drivername:
                raise ValueError(f"Driver with name '{drivername}' already exists.")
        # Create and add the new driver
        driver = Driver(name=drivername)
        self.btms.drivers.append(driver)
        return driver

    def create_route(self, number: int):
        # Check if a route with the same number already exists
        for route in self.btms.routes:
            if route.number == number:
                raise ValueError(f"Route with number '{number}' already exists.")
        # Create and add the new route
        route = Route(number=number)
        self.btms.routes.append(route)
        return route

    def create_route_assignment(self, licensePlate: str, route: int, _date: date):
        # Find the bus by license plate
        bus = None
        for v in self.btms.vehicles:
            if v.licencePlate == licensePlate:
                bus = v
                break
        if bus is None:
            raise ValueError(f"Bus with license plate '{licensePlate}' does not exist.")

        # Find the route by number
        route_obj = None
        for r in self.btms.routes:
            if r.number == route:
                route_obj = r
                break
        if route_obj is None:
            raise ValueError(f"Route with number '{route}' does not exist.")

        # Check if an assignment for this bus, route, and date already exists
        for assignment in self.btms.assignments:
            if (assignment.bus == bus and assignment.route == route_obj and assignment.date == _date):
                raise ValueError("Assignment for this bus, route, and date already exists.")

        # Create and add the new assignment
        assignment = RouteAssignment(date=_date, bus=bus, route=route_obj)
        self.btms.assignments.append(assignment)
        # Also add to bus and route assignments for bidirectional reference
        bus.assignments.append(assignment)
        route_obj.assignments.append(assignment)
        return assignment