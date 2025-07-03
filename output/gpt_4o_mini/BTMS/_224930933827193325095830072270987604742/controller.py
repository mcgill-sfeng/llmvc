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
        
        for route in self.btms.routes:
            if route.number == number:
                raise ValueError("A route with this number already exists. Please use a different number.")
        
        new_route = Route(number=number)
        self.btms.routes.append(new_route)

    def create_route_assignment(self, licensePlate: str, route: int, _date: date):
        # Check if the date is within one year from today
        today = date.today()
        if _date < today or _date > today + timedelta(days=365):
            raise ValueError("The date must be within a year from today.")
        
        # Check if the bus vehicle exists
        bus_vehicle = next((bv for bv in self.btms.vehicles if bv.licencePlate == licensePlate), None)
        if not bus_vehicle:
            raise ValueError("A bus must be specified for the assignment.")
        
        # Check if the route exists
        route_obj = next((r for r in self.btms.routes if r.number == route), None)
        if not route_obj:
            raise ValueError("A route must be specified for the assignment.")
        
        # Create the RouteAssignment
        new_assignment = RouteAssignment(date=_date, bus=bus_vehicle, route=route_obj)
        self.btms.assignments.append(new_assignment)
        bus_vehicle.assignments.append(new_assignment)
        route_obj.assignments.append(new_assignment)