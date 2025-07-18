from datetime import date
from assets.BTMS.model.umple import *

class BTMSController:
    def __init__(self):
        self.btms = BTMS()

    def create_driver(self, drivername: str):
        # Check if a driver with the same name already exists
        existing_driver = next((driver for driver in self.btms.drivers if driver.name == drivername), None)
        if existing_driver is not None:
            raise ValueError(f"Driver with name {drivername} already exists.")
        
        # Create a new driver
        new_driver = self.btms.Driver(drivername)
        self.btms.drivers.append(new_driver)

    def create_route(self, number: int):
        # Check if a route with the same number already exists
        existing_route = next((route for route in self.btms.routes if route.number == number), None)
        if existing_route is not None:
            raise ValueError(f"Route with number {number} already exists.")
        
        # Create a new route
        new_route = self.btms.Route(number)
        self.btms.routes.append(new_route)

    def create_route_assignment(self, licensePlate: str, route: int, _date: date):
        # Find the bus vehicle by license plate
        bus = next((vehicle for vehicle in self.btms.vehicles if vehicle.licencePlate == licensePlate), None)
        if bus is None:
            raise ValueError(f"No bus with license plate {licensePlate} found.")
        
        # Find the route by number
        route_obj = next((r for r in self.btms.routes if r.number == route), None)
        if route_obj is None:
            raise ValueError(f"No route with number {route} found.")
        
        # Check if an assignment already exists for the given bus, route, and date
        existing_assignment = next((assignment for assignment in self.btms.assignments 
                                    if assignment.bus == bus and assignment.route == route_obj and assignment.date == _date), None)
        if existing_assignment is not None:
            raise ValueError(f"Assignment for bus {licensePlate} on route {route} for date {_date} already exists.")
        
        # Create a new route assignment
        new_assignment = self.btms.RouteAssignment(_date, bus, route_obj)
        self.btms.assignments.append(new_assignment)