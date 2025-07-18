from datetime import date
from assets.BTMS.model.umple import *


class BTMSController:
    def __init__(self):
        self.btms = BTMS()

    def create_driver(self, drivername: str):
        if not drivername:
            raise ValueError("The name of a driver cannot be empty.")
        
        if Driver.hasWithName(drivername):
            raise ValueError("A driver with this name already exists.")
            
        return self.btms.addDriver(drivername)

    def create_route(self, number: int):
        if number <= 0:
            raise ValueError("The number of a route must be greater than zero.")
        if number > 9999:
            raise ValueError("The number of a route cannot be greater than 9999.")
            
        if Route.hasWithNumber(number):
            raise ValueError("A route with this number already exists. Please use a different number.")
            
        return self.btms.addRoute(number)

    def create_route_assignment(self, licensePlate: str, route: int, _date: date):
        # Validate inputs
        if not licensePlate:
            raise ValueError("A bus must be specified for the assignment.")
            
        if not route:
            raise ValueError("A route must be specified for the assignment.")
            
        # Check date is within a year from today
        today = date.today()
        one_year_later = date(today.year + 1, today.month, today.day)
        if _date < today or _date > one_year_later:
            raise ValueError("The date must be within a year from today.")
            
        # Get bus vehicle
        bus = BusVehicle.getWithLicencePlate(licensePlate)
        if not bus:
            raise ValueError(f"No bus found with license plate {licensePlate}")
            
        # Get route
        route_obj = Route.getWithNumber(route)
        if not route_obj:
            raise ValueError(f"No route found with number {route}")
            
        # Create assignment
        return self.btms.addAssignment(_date, bus, route_obj)