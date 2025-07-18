from datetime import date
from assets.BTMS.model.umple import *

class BTMSController:
    def __init__(self):
        self.btms = BTMS()

    def create_driver(self, drivername: str):
        # Validate the driver name
        if not drivername or drivername.strip() == "":
            raise ValueError("The name of a driver cannot be empty.")
        # Check if a driver with the same name already exists
        for i in range(self.btms.numberOfDrivers()):
            driver = self.btms.getDriver(i)
            if driver.getName() == drivername:
                # Driver already exists, do nothing or raise error if needed
                return
        # Add new driver
        self.btms.addDriver1(drivername)

    def create_route(self, number: int):
        # Validate the route number
        if not isinstance(number, int):
            raise ValueError("Route number must be an integer.")
        if number <= 0:
            raise ValueError("The number of a route must be greater than zero.")
        if number > 9999:
            raise ValueError("The number of a route cannot be greater than 9999.")
        # Check if route with same number exists
        for i in range(self.btms.numberOfRoutes()):
            route = self.btms.getRoute(i)
            if route.getNumber() == number:
                # Route with same number exists, throw error
                raise ValueError("A route with this number already exists. Please use a different number.")
        # Add new route
        self.btms.addRoute1(number)

    def create_route_assignment(self, licensePlate: str, route: int, _date: date):
        # Validate vehicle
        vehicle = None
        for i in range(self.btms.numberOfVehicles()):
            v = self.btms.getVehicle(i)
            if v.getLicencePlate() == licensePlate:
                vehicle = v
                break
        if vehicle is None:
            raise ValueError("A bus must be specified for the assignment.")
        # Validate route
        route_obj = None
        for i in range(self.btms.numberOfRoutes()):
            r = self.btms.getRoute(i)
            if r.getNumber() == route:
                route_obj = r
                break
        if route_obj is None:
            raise ValueError("A route must be specified for the assignment.")
        # Validate date: within one year from today
        today = date.today()
        delta_days = abs((_date - today).days)
        if delta_days > 365:
            raise ValueError("The date must be within a year from today.")
        # Create assignment
        self.btms.addAssignment1(_date, vehicle, route_obj)