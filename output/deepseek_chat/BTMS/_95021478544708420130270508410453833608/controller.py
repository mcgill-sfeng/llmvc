from datetime import date
from assets.BTMS.model.umple import *


class BTMSController:
    def __init__(self):
        self.btms = BTMS()

    def create_driver(self, drivername: str):
        """
        Creates a new driver with the given name.
        Returns the created Driver object or None if creation failed.
        """
        if not drivername or not isinstance(drivername, str):
            return None
        
        # Check if driver with this name already exists
        if Driver.hasWithName(drivername):
            return None
            
        return self.btms.addDriver1(drivername)

    def create_route(self, number: int):
        """
        Creates a new route with the given number.
        Returns the created Route object or None if creation failed.
        """
        if not isinstance(number, int) or number <= 0:
            return None
            
        # Check if route with this number already exists
        if Route.hasWithNumber(number):
            return None
            
        return self.btms.addRoute1(number)

    def create_route_assignment(self, licensePlate: str, route: int, _date: date):
        """
        Creates a new route assignment for a vehicle on a specific route and date.
        Returns the created RouteAssignment object or None if creation failed.
        """
        if (not isinstance(licensePlate, str) or (not isinstance(route, int)) or (not isinstance(_date, date))):
            return None
            
        # Check if vehicle exists
        if not BusVehicle.hasWithLicencePlate(licensePlate):
            return None
            
        # Check if route exists
        if not Route.hasWithNumber(route):
            return None
            
        # Get the actual objects
        vehicle = BusVehicle.getWithLicencePlate(licensePlate)
        route_obj = Route.getWithNumber(route)
        
        # Check if this assignment already exists
        for assignment in self.btms.getAssignments():
            if (assignment.getDate() == _date and 
                assignment.getBus() == vehicle and 
                assignment.getRoute() == route_obj):
                return None
                
        return self.btms.addAssignment1(_date, vehicle, route_obj)