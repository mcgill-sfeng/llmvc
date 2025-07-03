from datetime import date
from assets.BTMS.model.ecore import *


class BTMSController:
    def __init__(self):
        self.btms = BTMS()

    def create_driver(self, drivername: str):
        if not drivername:
            raise ValueError("The name of a driver cannot be empty.")
        
        # Assuming BTMS has a method to add drivers
        self.btms.drivers.append(self.btms.Driver(name=drivername))

    def create_route(self, number: int):
        if number <= 0:
            raise ValueError("The number of a route must be greater than zero.")
        if number > 9999:
            raise ValueError("The number of a route cannot be greater than 9999.")
        
        # Check if route with this number already exists
        if any(route.number == number for route in self.btms.routes):
            raise ValueError("A route with this number already exists. Please use a different number.")
        
        # Assuming BTMS has a method to add routes
        self.btms.routes.append(self.btms.Route(number=number))

    def create_route_assignment(self, licensePlate: str, route: int, _date: date):
        # Validate inputs
        if not licensePlate:
            raise ValueError("A bus must be specified for the assignment.")
        
        if not route:
            raise ValueError("A route must be specified for the assignment.")
        
        # Check date is within a year from today
        today = date.today()
        one_year_later = date(today.year + 1, today.month, today.day)
        if _date > one_year_later:
            raise ValueError("The date must be within a year from today.")
        
        # Check if bus exists and not in repair shop
        bus = next((v for v in self.btms.vehicles if v.licencePlate == licensePlate), None)
        if not bus:
            raise ValueError(f"Bus with license plate {licensePlate} not found.")
        # Assuming BusVehicle has an inRepairShop attribute
        if bus.inRepairShop:
            raise ValueError(f"Bus {licensePlate} is in repair shop and cannot be assigned.")
        
        # Check if route exists
        route_obj = next((r for r in self.btms.routes if r.number == route), None)
        if not route_obj:
            raise ValueError(f"Route {route} not found.")
        
        # Create the assignment
        assignment = self.btms.RouteAssignment(
            date=_date,
            bus=bus,
            route=route_obj
        )
        self.btms.assignments.append(assignment)
        
        # Add assignment to bus and route
        bus.assignments.append(assignment)
        route_obj.assignments.append(assignment)