from datetime import date, timedelta
from assets.BTMS.model.umple import *

class BTMSController:
    def __init__(self):
        self.btms = BTMS()

    def create_driver(self, drivername: str):
        # Validate the driver name
        if not drivername or drivername.strip() == "":
            raise ValueError("The name of a driver cannot be empty.")
        # Check for duplicate name
        if Driver.getWithName(drivername):
            # If driver with same name exists, do not create a new one
            # or raise error? Based on feature, should be error if duplicate
            # But scenario indicates no duplicate creation, so raise error
            raise ValueError("A driver with this name already exists.")
        # Create and add driver
        self.btms.addDriver(drivername)

    def create_route(self, number: int):
        # Validate route number
        if not isinstance(number, int):
            raise ValueError("Route number must be an integer.")
        if number <= 0:
            raise ValueError("The number of a route must be greater than zero.")
        if number > 9999:
            raise ValueError("The number of a route cannot be greater than 9999.")
        # Check for existing route with same number
        if Route.getWithNumber(number):
            # Already exists, throw error
            raise ValueError("A route with this number already exists. Please use a different number.")
        # Create and add route
        self.btms.addRoute(number)

    def create_route_assignment(self, licensePlate: str, route: int, _date: date):
        # Validate vehicle
        vehicle = BusVehicle.getWithLicencePlate(licensePlate)
        if vehicle is None:
            raise ValueError("A bus must be specified for the assignment.")
        # Validate route
        route_obj = Route.getWithNumber(route)
        if route_obj is None:
            raise ValueError("A route must be specified for the assignment.")
        # Validate date
        today = date.today()
        one_year_ago = today - timedelta(days=365)
        if _date < one_year_ago or _date > today + timedelta(days=365):
            raise ValueError("The date must be within a year from today.")
        # Create assignment
        self.btms.addAssignment(_date, vehicle, route_obj)