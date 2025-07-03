from datetime import date, timedelta
from assets.BTMS.model.umple import *

class BTMSController:
    def __init__(self):
        self.btms = BTMS()

    def create_driver(self, drivername: str):
        # Validate driver name
        if not drivername or drivername.strip() == "":
            raise Exception("The name of a driver cannot be empty.")
        # Check for uniqueness (the model will also enforce this, but we want the correct error message)
        if Driver.hasWithName(drivername):
            raise Exception("A driver with this name already exists. Please use a different name.")
        # Create driver
        self.btms.addDriver(drivername)

    def create_route(self, number: int):
        # Validate route number
        if number <= 0:
            raise Exception("The number of a route must be greater than zero.")
        if number > 9999:
            raise Exception("The number of a route cannot be greater than 9999.")
        # Check for uniqueness
        if Route.hasWithNumber(number):
            raise Exception("A route with this number already exists. Please use a different number.")
        # Create route
        self.btms.addRoute(number)

    def create_route_assignment(self, licensePlate: str, route: int, _date: date):
        # Validate bus vehicle existence
        bus = BusVehicle.getWithLicencePlate(licensePlate)
        if bus is None:
            raise Exception("A bus must be specified for the assignment.")
        # Validate route existence
        route_obj = Route.getWithNumber(route)
        if route_obj is None:
            raise Exception("A route must be specified for the assignment.")
        # Validate date: must be within one year from today (inclusive)
        today = date.today()
        min_date = today
        max_date = today + timedelta(days=365)
        if _date < min_date or _date > max_date:
            raise Exception("The date must be within a year from today.")
        # Create assignment
        self.btms.addAssignment(_date, bus, route_obj)