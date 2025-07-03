from datetime import date
from assets.BTMS.model.ecore import *


class BTMSController:
    def __init__(self):
        self.btms = BTMS()

    def create_driver(self, drivername: str):
        if not drivername:
            raise ValueError("The name of a driver cannot be empty.")
        
        # Assuming BTMS has a method to add drivers
        driver = Driver(name=drivername, schedules=[])
        self.btms.drivers.append(driver)

    def create_route(self, number: int):
        if number <= 0:
            raise ValueError("The number of a route must be greater than zero.")
        if number > 9999:
            raise ValueError("The number of a route cannot be greater than 9999.")
        
        # Check if route with this number already exists
        if any(route.number == number for route in self.btms.routes):
            raise ValueError("A route with this number already exists. Please use a different number.")
        
        # Assuming BTMS has a method to add routes
        route = Route(number=number, assignments=[])
        self.btms.routes.append(route)

    def create_route_assignment(self, licensePlate: str, route: int, _date: date):
        # Validate bus vehicle exists and is not in repair
        bus = next((v for v in self.btms.vehicles if v.licencePlate == licensePlate), None)
        if not bus:
            raise ValueError("A bus must be specified for the assignment.")
        if bus.inRepairShop:
            raise ValueError("Cannot assign a bus that's in the repair shop.")
        
        # Validate route exists
        route_obj = next((r for r in self.btms.routes if r.number == route), None)
        if not route_obj:
            raise ValueError("A route must be specified for the assignment.")
        
        # Validate date is within a year from today
        today = date(2021, 10, 7)  # As per background in the scenario
        if _date < today or _date > date(today.year + 1, today.month, today.day):
            raise ValueError("The date must be within a year from today.")
        
        # Check for existing assignment conflicts would go here
        
        # Create the assignment
        assignment = RouteAssignment(date=_date, bus=bus, route=route_obj, schedules=[])
        self.btms.assignments.append(assignment)
        bus.assignments.append(assignment)
        route_obj.assignments.append(assignment)