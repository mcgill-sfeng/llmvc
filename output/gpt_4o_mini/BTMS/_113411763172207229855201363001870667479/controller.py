from datetime import date, timedelta
from assets.BTMS.model.umple import *

class BTMSController:
    def __init__(self):
        self.btms = BTMS()

    def create_driver(self, drivername: str):
        if not drivername:
            raise ValueError("The name of a driver cannot be empty.")
        
        # Create and add the driver to the BTMS
        new_driver = Driver(drivername, self.btms)
        self.btms.addDriver2(new_driver)

    def create_route(self, number: int):
        if number <= 0:
            raise ValueError("The number of a route must be greater than zero.")
        if number > 9999:
            raise ValueError("The number of a route cannot be greater than 9999.")
        if self.btms.getRoute(number - 1) is not None:  # Check if route already exists
            raise ValueError("A route with this number already exists. Please use a different number.")
        
        # Create and add the route to the BTMS
        new_route = Route(number, self.btms)
        self.btms.addRoute2(new_route)

    def create_route_assignment(self, licensePlate: str, route: int, _date: date):
        # Validate the bus vehicle
        vehicle = next((v for v in self.btms.getVehicles() if v.getLicencePlate() == licensePlate), None)
        if vehicle is None:
            raise ValueError("A bus must be specified for the assignment.")
        
        # Validate the route
        route_obj = next((r for r in self.btms.getRoutes() if r.getNumber() == route), None)
        if route_obj is None:
            raise ValueError("A route must be specified for the assignment.")
        
        # Validate the date
        current_date = date.today()
        if _date < current_date or _date > current_date + timedelta(days=365):
            raise ValueError("The date must be within a year from today.")
        
        # Create and add the route assignment to the BTMS
        new_assignment = RouteAssignment(_date, vehicle, route_obj, self.btms)
        self.btms.addAssignment2(new_assignment)