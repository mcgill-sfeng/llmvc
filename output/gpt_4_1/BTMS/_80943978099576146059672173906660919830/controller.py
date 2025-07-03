from datetime import date, timedelta
from assets.BTMS.model.umple import *

class BTMSController:
    def __init__(self):
        self.btms = BTMS()

    def create_driver(self, drivername: str):
        # Check for empty name
        if not drivername or drivername.strip() == "":
            raise Exception("The name of a driver cannot be empty.")
        # Check for uniqueness
        for driver in self.btms.getDrivers():
            if driver.getName() == drivername:
                # The requirements do not specify error for duplicate names, but the model says unique
                # We'll allow only one driver with a given name
                raise Exception("A driver with this name already exists. Please use a different name.")
        # Add driver
        self.btms.addDriver1(drivername)

    def create_route(self, number: int):
        # Validate number
        if number <= 0:
            raise Exception("The number of a route must be greater than zero.")
        if number > 9999:
            raise Exception("The number of a route cannot be greater than 9999.")
        # Check uniqueness
        for route in self.btms.getRoutes():
            if route.getNumber() == number:
                raise Exception("A route with this number already exists. Please use a different number.")
        # Add route
        self.btms.addRoute1(number)

    def create_route_assignment(self, licensePlate: str, route: int, _date: date):
        # Validate bus vehicle
        bus = None
        for v in self.btms.getVehicles():
            if v.getLicencePlate() == licensePlate:
                bus = v
                break
        if bus is None:
            raise Exception("A bus must be specified for the assignment.")

        # Validate route
        route_obj = None
        for r in self.btms.getRoutes():
            if r.getNumber() == route:
                route_obj = r
                break
        if route_obj is None:
            raise Exception("A route must be specified for the assignment.")

        # Validate date: must be within one year from today (inclusive)
        today = date.today()
        min_date = today
        max_date = today + timedelta(days=365)
        if _date < min_date or _date > max_date:
            raise Exception("The date must be within a year from today.")

        # Add assignment
        self.btms.addAssignment1(_date, bus, route_obj)