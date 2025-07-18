from datetime import date, timedelta
from assets.BTMS.model.umple import *

class BTMSController:
    def __init__(self):
        self.btms = BTMS()

    def create_driver(self, drivername: str):
        # Validate driver name
        if drivername is None or drivername.strip() == "":
            raise Exception("The name of a driver cannot be empty.")
        # Add driver using model-layer method
        self.btms.addDriver1(drivername)

    def create_route(self, number: int):
        # Validate route number
        if number <= 0:
            raise Exception("The number of a route must be greater than zero.")
        if number > 9999:
            raise Exception("The number of a route cannot be greater than 9999.")
        # Check for duplicate route number
        for i in range(self.btms.numberOfRoutes()):
            route = self.btms.getRoute(i)
            if route.getNumber() == number:
                raise Exception("A route with this number already exists. Please use a different number.")
        # Add route using model-layer method
        self.btms.addRoute1(number)

    def create_route_assignment(self, licensePlate: str, route: int, _date: date):
        # Validate bus vehicle existence
        bus = None
        for i in range(self.btms.numberOfVehicles()):
            v = self.btms.getVehicle(i)
            if v.getLicencePlate() == licensePlate:
                bus = v
                break
        if bus is None:
            raise Exception("A bus must be specified for the assignment.")

        # Validate route existence
        route_obj = None
        for i in range(self.btms.numberOfRoutes()):
            r = self.btms.getRoute(i)
            if r.getNumber() == route:
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

        # Add assignment using model-layer method
        self.btms.addAssignment1(_date, bus, route_obj)