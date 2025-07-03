from datetime import date, timedelta
from assets.BTMS.model.umple import *

class BTMSController:
    def __init__(self):
        self.btms = BTMS()

    def create_driver(self, drivername: str):
        # Validate name
        if drivername is None or drivername.strip() == "":
            raise ValueError("The name of a driver cannot be empty.")
        # Check for duplicate (model will also enforce, but we want to raise the correct error)
        if Driver.hasWithName(drivername):
            # Defensive: Should not happen in normal use, but let's be explicit
            raise ValueError("A driver with this name already exists.")
        # Create driver
        self.btms.addDriver(drivername)
        # No return needed; test expects no error

    def create_route(self, number: int):
        # Validate number
        if not isinstance(number, int):
            raise ValueError("The number of a route must be an integer.")
        if number <= 0:
            raise ValueError("The number of a route must be greater than zero.")
        if number > 9999:
            raise ValueError("The number of a route cannot be greater than 9999.")
        # Check for duplicate
        if Route.hasWithNumber(number):
            raise ValueError("A route with this number already exists. Please use a different number.")
        # Create route
        self.btms.addRoute(number)
        # No return needed; test expects no error

    def create_route_assignment(self, licensePlate: str, route: int, _date: date):
        # Validate bus
        bus = BusVehicle.getWithLicencePlate(licensePlate)
        if bus is None:
            raise ValueError("A bus must be specified for the assignment.")
        # Validate route
        route_obj = Route.getWithNumber(route)
        if route_obj is None:
            raise ValueError("A route must be specified for the assignment.")
        # Validate date
        # The date must be within a year from today (inclusive of today? Let's assume exclusive, as per usual business logic)
        today = date.today()
        # Acceptable: from today (inclusive) up to 365 days in the future (inclusive)
        min_date = today
        max_date = today + timedelta(days=365)
        if _date < min_date or _date > max_date:
            raise ValueError("The date must be within a year from today.")
        # Create assignment
        self.btms.addAssignment(_date, bus, route_obj)
        # No return needed; test expects no error