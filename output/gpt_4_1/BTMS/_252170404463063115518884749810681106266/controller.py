from datetime import date, timedelta
from assets.BTMS.model.ecore import *

class BTMSController:
    def __init__(self):
        self.btms = BTMS()

    def create_driver(self, drivername: str):
        if not drivername or drivername.strip() == "":
            raise Exception("The name of a driver cannot be empty.")
        self.btms.add_driver(drivername)

    def create_route(self, number: int):
        if number <= 0:
            raise Exception("The number of a route must be greater than zero.")
        if number > 9999:
            raise Exception("The number of a route cannot be greater than 9999.")
        # Check for duplicate route number
        for route in self.btms.get_routes():
            if route.get_number() == number:
                raise Exception("A route with this number already exists. Please use a different number.")
        self.btms.add_route(number)

    def create_route_assignment(self, licensePlate: str, route: int, _date: date):
        # Validate bus vehicle
        bus = None
        for vehicle in self.btms.get_bus_vehicles():
            if vehicle.get_license_plate() == licensePlate:
                bus = vehicle
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

        # Validate date: must be within one year from today
        today = self.btms.get_current_date() if hasattr(self.btms, "get_current_date") else date.today()
        min_date = today
        max_date = today + timedelta(days=365)
        if _date < min_date or _date > max_date:
            raise Exception("The date must be within a year from today.")

        self.btms.add_route_assignment(bus, route_obj, _date)