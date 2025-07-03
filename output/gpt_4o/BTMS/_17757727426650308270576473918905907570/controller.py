from datetime import date, timedelta
from assets.BTMS.model.umple import *

class BTMSController:
    def __init__(self):
        self.btms = BTMS()

    def create_driver(self, drivername: str):
        if not drivername:
            raise ValueError("The name of a driver cannot be empty.")
        
        # Assuming BTMS has a method to add a driver
        driver = Driver(drivername)
        self.btms.add_driver(driver)

    def create_route(self, number: int):
        if number <= 0:
            raise ValueError("The number of a route must be greater than zero.")
        if number > 9999:
            raise ValueError("The number of a route cannot be greater than 9999.")
        
        # Check if a route with the same number already exists
        for route in self.btms.routes:
            if route.number == number:
                raise ValueError("A route with this number already exists. Please use a different number.")
        
        # Assuming BTMS has a method to add a route
        route = Route(number)
        self.btms.add_route(route)

    def create_route_assignment(self, licensePlate: str, route: int, _date: date):
        # Check if the date is within a year from today
        today = date.today()
        if not (today <= _date <= today + timedelta(days=365)):
            raise ValueError("The date must be within a year from today.")
        
        # Find the bus vehicle by license plate
        bus = None
        for vehicle in self.btms.vehicles:
            if vehicle.licencePlate == licensePlate:
                bus = vehicle
                break
        if not bus:
            raise ValueError("A bus must be specified for the assignment.")
        
        # Find the route by number
        route_obj = None
        for r in self.btms.routes:
            if r.number == route:
                route_obj = r
                break
        if not route_obj:
            raise ValueError("A route must be specified for the assignment.")
        
        # Assuming BTMS has a method to add a route assignment
        assignment = RouteAssignment(_date, bus, route_obj)
        self.btms.add_assignment(assignment)