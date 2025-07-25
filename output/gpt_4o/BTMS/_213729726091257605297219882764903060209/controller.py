from datetime import date, timedelta
from assets.BTMS.model.ecore import *


class BTMSController:
    def __init__(self):
        self.btms = BTMS(vehicles=[], routes=[], assignments=[], drivers=[], schedules=[])

    def create_driver(self, drivername: str):
        if not drivername:
            raise ValueError("The name of a driver cannot be empty.")
        
        new_driver = Driver(name=drivername, schedules=[])
        self.btms.drivers.append(new_driver)

    def create_route(self, number: int):
        if number <= 0:
            raise ValueError("The number of a route must be greater than zero.")
        if number > 9999:
            raise ValueError("The number of a route cannot be greater than 9999.")
        
        for route in self.btms.routes:
            if route.number == number:
                raise ValueError("A route with this number already exists. Please use a different number.")
        
        new_route = Route(number=number, assignments=[])
        self.btms.routes.append(new_route)

    def create_route_assignment(self, licensePlate: str, route: int, _date: date):
        # Check if the date is within a year from today
        today = date.today()
        if not (today <= _date <= today + timedelta(days=365)):
            raise ValueError("The date must be within a year from today.")
        
        # Find the bus vehicle
        bus = None
        for vehicle in self.btms.vehicles:
            if vehicle.licencePlate == licensePlate:
                bus = vehicle
                break
        if not bus:
            raise ValueError("A bus must be specified for the assignment.")
        
        # Check if the bus is in the repair shop
        if getattr(bus, 'inRepairShop', False):
            raise ValueError("The bus is currently in the repair shop and cannot be assigned.")
        
        # Find the route
        route_obj = None
        for r in self.btms.routes:
            if r.number == route:
                route_obj = r
                break
        if not route_obj:
            raise ValueError("A route must be specified for the assignment.")
        
        # Create the route assignment
        new_assignment = RouteAssignment(date=_date, bus=bus, route=route_obj, schedules=[])
        self.btms.assignments.append(new_assignment)
        bus.assignments.append(new_assignment)
        route_obj.assignments.append(new_assignment)