from datetime import date, timedelta
from assets.BTMS.model.umple import *

class BTMSController:
    def __init__(self):
        self.btms = BTMS()

    def create_driver(self, drivername: str):
        if not drivername or drivername.strip() == "":
            raise Exception("The name of a driver cannot be empty.")
        # Assuming BTMS has add_driver(name) and get_drivers()
        self.btms.add_driver(drivername)

    def create_route(self, number: int):
        if number <= 0:
            raise Exception("The number of a route must be greater than zero.")
        if number > 9999:
            raise Exception("The number of a route cannot be greater than 9999.")
        # Check for duplicate route number
        # Assuming BTMS has get_routes() returning iterable of route objects with .get_number()
        for route in self.btms.get_routes():
            if hasattr(route, "get_number"):
                route_number = route.get_number()
            else:
                route_number = route.number  # fallback
            if route_number == number:
                raise Exception("A route with this number already exists. Please use a different number.")
        # Assuming BTMS has add_route(number)
        self.btms.add_route(number)

    def create_route_assignment(self, licensePlate: str, route: int, _date: date):
        # Validate bus vehicle
        bus = None
        for v in self.btms.get_bus_vehicles():
            lp = v.get_licence_plate() if hasattr(v, "get_licence_plate") else v.licencePlate
            if lp == licensePlate:
                bus = v
                break
        if bus is None:
            raise Exception("A bus must be specified for the assignment.")

        # Validate route
        route_obj = None
        for r in self.btms.get_routes():
            rnum = r.get_number() if hasattr(r, "get_number") else r.number
            if rnum == route:
                route_obj = r
                break
        if route_obj is None:
            raise Exception("A route must be specified for the assignment.")

        # Validate date: must be within a year from today (either direction)
        today = date.today()
        delta = abs((_date - today).days)
        if delta > 365:
            raise Exception("The date must be within a year from today.")

        # Assuming BTMS has add_route_assignment(bus, route, date)
        self.btms.add_route_assignment(bus, route_obj, _date)