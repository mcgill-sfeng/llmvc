from datetime import date, timedelta
from assets.BTMS.model.umple import *

class BTMSController:
    def __init__(self):
        self.btms = BTMS()

    def create_driver(self, drivername: str):
        # Create a new Driver with the given name and add to BTMS
        driver = self.btms.createDriver(drivername)
        return driver

    def create_route(self, number: int):
        # Create a new Route with the given number and add to BTMS
        route = self.btms.createRoute(number)
        return route

    def create_route_assignment(self, licensePlate: str, route: int, _date: date):
        # Validate date: must be within one year from today
        today = date.today()
        one_year_later = today + timedelta(days=365)
        if not (_date >= today and _date <= one_year_later):
            raise ValueError("Date must be within one year from today.")

        # Create BusVehicle with licensePlate
        bus_vehicle = self.btms.createBusVehicle(licensePlate)

        # Create Route with route number
        route_obj = self.btms.createRoute(route)

        # Create RouteAssignment with date, bus, and route
        route_assignment = self.btms.createRouteAssignment(_date, bus_vehicle, route_obj)

        return route_assignment