from datetime import date, timedelta
from assets.BTMS.model.umple import *


class BTMSController:
    def __init__(self):
        self.btms = BTMS()

    def create_driver(self, drivername: str):
        if not drivername:
            raise ValueError("The name of a driver cannot be empty.")
        
        if Driver.hasWithName(drivername):
            raise ValueError("A driver with this name already exists.")
            
        self.btms.addDriver1(drivername)

    def create_route(self, number: int):
        if number <= 0:
            raise ValueError("The number of a route must be greater than zero.")
        if number > 9999:
            raise ValueError("The number of a route cannot be greater than 9999.")
            
        if Route.hasWithNumber(number):
            raise ValueError("A route with this number already exists. Please use a different number.")
            
        self.btms.addRoute1(number)

    def create_route_assignment(self, licensePlate: str, route: int, _date: date):
        # Validate bus vehicle exists
        if not BusVehicle.hasWithLicencePlate(licensePlate):
            raise ValueError("A bus must be specified for the assignment.")
            
        # Validate route exists
        if not Route.hasWithNumber(route):
            raise ValueError("A route must be specified for the assignment.")
            
        # Validate date is within one year from today
        today = date(2035, 1, 1)  # Assuming current year is 2035 as per the prompt
        one_year_later = today + timedelta(days=365)
        
        if _date < today or _date > one_year_later:
            raise ValueError("The date must be within a year from today.")
            
        # Get the bus and route objects
        bus = BusVehicle.getWithLicencePlate(licensePlate)
        route_obj = Route.getWithNumber(route)
        
        # Check if the bus is in repair shop
        # Note: This check would require additional model layer support not shown in the provided interface
        # Assuming we can check this somehow, perhaps through a method like bus.isInRepairShop()
        # For now, we'll skip this check since it's not in the model interface provided
        
        # Create the assignment
        self.btms.addAssignment1(_date, bus, route_obj)