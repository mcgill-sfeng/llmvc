from datetime import date
from assets.BTMS.model.ecore import *


class BTMSController:
    def __init__(self):
        self.btms = BTMS()

    def create_driver(self, drivername: str):
        # Check if the driver already exists
        for driver in self.btms.drivers:
            if driver.name == drivername:
                raise ValueError(f"Driver '{drivername}' already exists.")
        
        # Create a new driver and add to the BTMS
        new_driver = Driver(name=drivername)
        self.btms.drivers.append(new_driver)

    def create_route(self, number: int):
        # Check if the route already exists
        for route in self.btms.routes:
            if route.number == number:
                raise ValueError(f"Route number '{number}' already exists.")
        
        # Create a new route and add to the BTMS
        new_route = Route(number=number)
        self.btms.routes.append(new_route)

    def create_route_assignment(self, licensePlate: str, route: int, _date: date):
        # Find the bus vehicle by license plate
        bus = next((vehicle for vehicle in self.btms.vehicles if vehicle.licencePlate == licensePlate), None)
        if bus is None:
            raise ValueError(f"Bus with license plate '{licensePlate}' does not exist.")

        # Find the route by number
        route_obj = next((r for r in self.btms.routes if r.number == route), None)
        if route_obj is None:
            raise ValueError(f"Route number '{route}' does not exist.")

        # Check if an assignment for this bus and route on the given date already exists
        for assignment in self.btms.assignments:
            if assignment.bus == bus and assignment.route == route_obj and assignment.date == _date:
                raise ValueError(f"Assignment for bus '{licensePlate}' on route '{route}' for date '{_date}' already exists.")

        # Create a new route assignment and add to the BTMS
        new_assignment = RouteAssignment(date=_date, bus=bus, route=route_obj)
        self.btms.assignments.append(new_assignment)