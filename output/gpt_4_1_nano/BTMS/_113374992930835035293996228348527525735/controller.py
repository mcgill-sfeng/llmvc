from datetime import date, timedelta
from assets.BTMS.model.umple import *

class BTMSController:
    def __init__(self):
        self.btms = BTMS()

    def create_driver(self, drivername: str):
        # Validate driver name
        if not drivername or drivername.strip() == "":
            raise ValueError("The name of a driver cannot be empty.")
        # Create and add driver
        driver = Driver(name=drivername.strip())
        self.btms.addDriver(driver)

    def create_route(self, number: int):
        # Validate route number
        if not isinstance(number, int):
            raise ValueError("Route number must be an integer.")
        if number <= 0:
            raise ValueError("The number of a route must be greater than zero.")
        if number > 9999:
            raise ValueError("The number of a route cannot be greater than 9999.")
        # Check for existing route with same number
        existing_routes = self.btms.getRoutes()
        for route in existing_routes:
            if route.number == number:
                raise ValueError("A route with this number already exists. Please use a different number.")
        # Create and add route
        route = Route(number=number)
        self.btms.addRoute(route)

    def create_route_assignment(self, licensePlate: str, route: int, _date: date):
        # Validate vehicle existence
        vehicles = self.btms.getVehicles()
        vehicle = None
        for v in vehicles:
            if v.licencePlate == licensePlate:
                vehicle = v
                break
        if vehicle is None:
            raise ValueError("A bus must be specified for the assignment.")
        # Validate route existence
        routes = self.btms.getRoutes()
        route_obj = None
        for r in routes:
            if r.number == route:
                route_obj = r
                break
        if route_obj is None:
            raise ValueError("A route must be specified for the assignment.")
        # Validate date within one year from today
        today = date.today()
        delta_days = abs((today - _date).days)
        if delta_days > 365:
            raise ValueError("The date must be within a year from today.")
        # Create RouteAssignment
        assignment = RouteAssignment(date=_date)
        assignment.setBus(vehicle)
        assignment.setRoute(route_obj)
        self.btms.addAssignment(assignment)