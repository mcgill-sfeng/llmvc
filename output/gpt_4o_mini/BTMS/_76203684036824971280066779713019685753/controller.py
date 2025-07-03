from datetime import date, timedelta
from assets.BTMS.model.umple import *

class BTMSController:
    def __init__(self):
        self.btms = BTMS()

    def create_driver(self, drivername: str):
        if not drivername:
            raise ValueError("The name of a driver cannot be empty.")
        new_driver = Driver(name=drivername)
        self.btms.drivers.add(new_driver)

    def create_route(self, number: int):
        if number <= 0:
            raise ValueError("The number of a route must be greater than zero.")
        if number > 9999:
            raise ValueError("The number of a route cannot be greater than 9999.")
        existing_route = next((route for route in self.btms.routes if route.number == number), None)
        if existing_route:
            raise ValueError("A route with this number already exists. Please use a different number.")
        new_route = Route(number=number)
        self.btms.routes.add(new_route)

    def create_route_assignment(self, licensePlate: str, route: int, _date: date):
        if not licensePlate:
            raise ValueError("A bus must be specified for the assignment.")
        bus = next((vehicle for vehicle in self.btms.vehicles if vehicle.licencePlate == licensePlate), None)
        if not bus:
            raise ValueError("A bus must be specified for the assignment.")
        if bus.inRepairShop:
            raise ValueError("The bus is currently in the repair shop and cannot be assigned.")
        
        route_obj = next((r for r in self.btms.routes if r.number == route), None)
        if not route_obj:
            raise ValueError("A route must be specified for the assignment.")
        
        today = date.today()
        if _date < today or _date > today + timedelta(days=365):
            raise ValueError("The date must be within a year from today.")
        
        new_assignment = RouteAssignment(date=_date, bus=bus, route=route_obj)
        self.btms.assignments.add(new_assignment)