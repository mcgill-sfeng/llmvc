from datetime import date, timedelta
from assets.BTMS.model.umple import *

class BTMSController:
    def __init__(self):
        self.btms = BTMS()

    def create_driver(self, drivername: str):
        if not drivername:
            raise ValueError("The name of a driver cannot be empty.")
        self.btms.addDriver1(drivername)

    def create_route(self, number: int):
        if number <= 0:
            raise ValueError("The number of a route must be greater than zero.")
        if number > 9999:
            raise ValueError("The number of a route cannot be greater than 9999.")
        if any(route.getNumber() == number for route in self.btms.getRoutes()):
            raise ValueError("A route with this number already exists. Please use a different number.")
        self.btms.addRoute1(number)

    def create_route_assignment(self, licensePlate: str, route: int, _date: date):
        # Check if the vehicle exists and is not in the repair shop
        vehicle = next((v for v in self.btms.getVehicles() if v.getLicencePlate() == licensePlate), None)
        if not vehicle:
            raise ValueError("A bus must be specified for the assignment.")
        if any(v.getLicencePlate() == licensePlate and v.inRepairShop for v in self.btms.getVehicles()):
            raise ValueError("The specified bus is in the repair shop.")

        # Check if the route exists
        route_obj = next((r for r in self.btms.getRoutes() if r.getNumber() == route), None)
        if not route_obj:
            raise ValueError("A route must be specified for the assignment.")

        # Check if the date is within a year from today
        today = date.today()
        if not (today <= _date <= today + timedelta(days=365)):
            raise ValueError("The date must be within a year from today.")

        # Create the route assignment
        self.btms.addAssignment1(_date, vehicle, route_obj)