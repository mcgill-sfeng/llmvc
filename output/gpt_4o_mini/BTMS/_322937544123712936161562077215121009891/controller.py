from datetime import date, timedelta
from assets.BTMS.model.ecore import *

class BTMSController:
    def __init__(self):
        self.btms = BTMS()

    def create_driver(self, drivername: str):
        if not drivername:
            raise ValueError("The name of a driver cannot be empty.")
        
        new_driver = Driver(name=drivername)
        self.btms.drivers.append(new_driver)

    def create_route(self, number: int):
        if number <= 0:
            raise ValueError("The number of a route must be greater than zero.")
        if number > 9999:
            raise ValueError("The number of a route cannot be greater than 9999.")
        
        # Check for existing route with the same number
        for route in self.btms.routes:
            if route.number == number:
                raise ValueError("A route with this number already exists. Please use a different number.")
        
        new_route = Route(number=number)
        self.btms.routes.append(new_route)

    def create_route_assignment(self, licensePlate: str, route: int, _date: date):
        # Validate vehicle
        vehicle = next((v for v in self.btms.vehicles if v.licencePlate == licensePlate), None)
        if vehicle is None:
            raise ValueError("A bus must be specified for the assignment.")
        
        # Validate route
        route_obj = next((r for r in self.btms.routes if r.number == route), None)
        if route_obj is None:
            raise ValueError("A route must be specified for the assignment.")
        
        # Validate date
        today = date.today()
        if _date < today or _date > today + timedelta(days=365):
            raise ValueError("The date must be within a year from today.")
        
        new_assignment = RouteAssignment(date=_date, bus=vehicle, route=route_obj)
        self.btms.assignments.append(new_assignment)
        vehicle.assignments.append(new_assignment)
        route_obj.assignments.append(new_assignment)