from datetime import date
from assets.BTMS.model.umple import *


class BTMSController:
    def __init__(self):
        self.btms = BTMS()

    def create_driver(self, drivername: str):
        """
        Creates a new driver with the given name and adds it to the BTMS system.
        
        Args:
            drivername (str): The name of the driver to create
            
        Returns:
            bool: True if driver was created successfully, False if driver already exists
        """
        if Driver.hasWithName(drivername):
            return False
        self.btms.addDriver1(drivername)
        return True

    def create_route(self, number: int):
        """
        Creates a new route with the given number and adds it to the BTMS system.
        
        Args:
            number (int): The route number to create
            
        Returns:
            bool: True if route was created successfully, False if route already exists
        """
        if Route.hasWithNumber(number):
            return False
        self.btms.addRoute1(number)
        return True

    def create_route_assignment(self, licensePlate: str, route: int, _date: date):
        """
        Creates a new route assignment for a vehicle on a specific date.
        
        Args:
            licensePlate (str): The vehicle's license plate
            route (int): The route number
            _date (date): The date of the assignment
            
        Returns:
            bool: True if assignment was created successfully, False if any required elements don't exist
        """
        # Check if vehicle exists
        if not BusVehicle.hasWithLicencePlate(licensePlate):
            return False
            
        # Check if route exists
        if not Route.hasWithNumber(route):
            return False
            
        # Get the actual vehicle and route objects
        vehicle = BusVehicle.getWithLicencePlate(licensePlate)
        route_obj = Route.getWithNumber(route)
        
        # Create the assignment
        self.btms.addAssignment1(_date, vehicle, route_obj)
        return True