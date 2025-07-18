from datetime import date, timedelta
from assets.BTMS.model.umple import *

class BTMSController:
    def __init__(self):
        self.btms = BTMS()

    def create_driver(self, drivername: str):
        # Create a new Driver with the given name
        self.btms.addDriver1(drivername)

    def create_route(self, number: int):
        # Create a new Route with the given number
        self.btms.addRoute1(number)

    def create_route_assignment(self, licensePlate: str, route: int, _date: date):
        # Validate date: must be within one year from today
        today = date.today()
        one_year_later = today + timedelta(days=365)
        if _date < today or _date > one_year_later:
            raise ValueError("Date must be within one year from today.")

        # Retrieve the BusVehicle by licensePlate
        vehicle = None
        for v in self.btms.getVehicles():
            if v.getLicencePlate() == licensePlate:
                vehicle = v
                break
        if vehicle is None:
            # If not found, create and add new vehicle
            self.btms.addVehicle1(licensePlate)
            # Retrieve again after creation
            for v in self.btms.getVehicles():
                if v.getLicencePlate() == licensePlate:
                    vehicle = v
                    break
            if vehicle is None:
                raise RuntimeError("Failed to create or retrieve BusVehicle.")

        # Retrieve the Route by number
        route_obj = None
        for r in self.btms.getRoutes():
            if r.getNumber() == route:
                route_obj = r
                break
        if route_obj is None:
            # If not found, create and add new route
            self.btms.addRoute1(route)
            for r in self.btms.getRoutes():
                if r.getNumber() == route:
                    route_obj = r
                    break
            if route_obj is None:
                raise RuntimeError("Failed to create or retrieve Route.")

        # Create the RouteAssignment
        self.btms.addAssignment1(_date, vehicle, route_obj)