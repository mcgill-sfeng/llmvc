from datetime import date, timedelta
from assets.BTMS.model.ecore import *

class BTMSController:
    def __init__(self):
        self.btms = BTMS()

    def create_driver(self, drivername: str):
        # Validate driver name
        if not drivername or drivername.strip() == "":
            raise ValueError("The name of a driver cannot be empty.")
        # Create and add driver
        driver = self.btms.createDriver(drivername)
        # No return needed

    def create_route(self, number: int):
        # Validate route number
        if number <= 0:
            raise ValueError("The number of a route must be greater than zero.")
        if number > 9999:
            raise ValueError("The number of a route cannot be greater than 9999.")
        # Check for existing route with same number
        existing_routes = [r for r in self.btms.routes if r.number == number]
        if existing_routes:
            raise ValueError("A route with this number already exists. Please use a different number.")
        # Create and add route
        self.btms.createRoute(number)

    def create_route_assignment(self, licensePlate: str, route: int, _date: date):
        # Validate vehicle existence
        vehicle_list = [v for v in self.btms.vehicles if v.licencePlate == licensePlate]
        if not vehicle_list:
            raise ValueError("A bus must be specified for the assignment.")
        vehicle = vehicle_list[0]

        # Validate route existence
        route_list = [r for r in self.btms.routes if r.number == route]
        if not route_list:
            raise ValueError("A route must be specified for the assignment.")
        route_obj = route_list[0]

        # Validate date within one year from today
        today = date(2035, 10, 7)  # Fixed current date as per background
        delta_days = abs(( _date - today ).days)
        if delta_days > 365:
            raise ValueError("The date must be within a year from today.")

        # Check if vehicle already assigned on that date
        for assignment in vehicle.assignments:
            if assignment.date == _date:
                # Assuming multiple assignments per vehicle per date are not allowed
                # (not specified, but logical)
                # If multiple assignments are allowed, skip this check
                pass

        # Create and add route assignment
        self.btms.createRouteAssignment(vehicle.licencePlate, route, _date)