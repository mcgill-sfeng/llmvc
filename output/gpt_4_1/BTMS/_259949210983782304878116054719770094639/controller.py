from datetime import date, timedelta
from assets.BTMS.model.umple import *

class BTMSController:
    def __init__(self):
        self.btms = BTMS()

    def create_driver(self, drivername: str):
        if not drivername or drivername.strip() == "":
            raise Exception("The name of a driver cannot be empty.")
        # Check for uniqueness of driver name is not required by requirements
        self.btms.add_driver(drivername)

    def create_route(self, number: int):
        if number <= 0:
            raise Exception("The number of a route must be greater than zero.")
        if number > 9999:
            raise Exception("The number of a route cannot be greater than 9999.")
        # Check if route with this number already exists
        for route in self.btms.get_routes():
            if route.get_number() == number:
                raise Exception("A route with this number already exists. Please use a different number.")
        self.btms.add_route(number)

    def create_route_assignment(self, licensePlate: str, route: int, _date: date):
        # Validate bus vehicle
        bus = None
        for v in self.btms.get_bus_vehicles():
            if v.get_license_plate() == licensePlate:
                bus = v
                break
        if bus is None:
            raise Exception("A bus must be specified for the assignment.")

        # Validate route
        route_obj = None
        for r in self.btms.get_routes():
            if r.get_number() == route:
                route_obj = r
                break
        if route_obj is None:
            raise Exception("A route must be specified for the assignment.")

        # Validate date: must be within a year from today (inclusive)
        today = date.today()
        min_date = today
        max_date = today + timedelta(days=365)
        if _date < min_date or _date > max_date:
            raise Exception("The date must be within a year from today.")

        # Create assignment
        self.btms.add_route_assignment(bus, route_obj, _date)