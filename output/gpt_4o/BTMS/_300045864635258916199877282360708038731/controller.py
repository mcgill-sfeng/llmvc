from datetime import date, timedelta
from assets.BTMS.model.umple import *

class BTMSController:
    def __init__(self):
        self.btms = BTMS()

    def create_driver(self, drivername: str):
        if not drivername:
            raise ValueError("Driver name cannot be empty.")
        if Driver.hasWithName(drivername):
            raise ValueError(f"Driver with name '{drivername}' already exists.")
        self.btms.addDriver(drivername)

    def create_route(self, number: int):
        if not (1 <= number <= 9999):
            raise ValueError("Route number must be between 1 and 9999.")
        if Route.hasWithNumber(number):
            raise ValueError(f"Route with number '{number}' already exists.")
        self.btms.addRoute(number)

    def create_route_assignment(self, licensePlate: str, route: int, _date: date):
        if not BusVehicle.hasWithLicencePlate(licensePlate):
            raise ValueError(f"Bus with license plate '{licensePlate}' does not exist.")
        if not Route.hasWithNumber(route):
            raise ValueError(f"Route with number '{route}' does not exist.")
        
        today = date.today()
        one_year_from_today = today + timedelta(days=365)
        if not (today <= _date <= one_year_from_today):
            raise ValueError("Date must be within one year from today.")
        
        bus = BusVehicle.getWithLicencePlate(licensePlate)
        route_obj = Route.getWithNumber(route)
        self.btms.addAssignment(_date, bus, route_obj)