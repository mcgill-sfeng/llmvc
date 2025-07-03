from datetime import date
from assets.BTMS.model.umple import *


class BTMSController:
    def __init__(self):
        self.btms = BTMS()

    def create_driver(self, drivername: str):
        """
        Creates a new driver with the given name.
        
        Args:
            drivername: The name of the driver to create
            
        Returns:
            The created Driver object or None if creation failed
        """
        if not drivername or not isinstance(drivername, str):
            return None
            
        try:
            return self.btms.addDriver(drivername)
        except RuntimeError:
            # Driver with this name already exists
            return None

    def create_route(self, number: int):
        """
        Creates a new route with the given number.
        
        Args:
            number: The route number to create
            
        Returns:
            The created Route object or None if creation failed
        """
        if not isinstance(number, int) or number < 0:
            return None
            
        try:
            return self.btms.addRoute(number)
        except RuntimeError:
            # Route with this number already exists
            return None

    def create_route_assignment(self, licensePlate: str, route: int, _date: date):
        """
        Creates a new route assignment for a vehicle on a specific date.
        
        Args:
            licensePlate: The vehicle's license plate
            route: The route number to assign
            _date: The date of the assignment
            
        Returns:
            The created RouteAssignment object or None if creation failed
        """
        if (not isinstance(licensePlate, str) or (not isinstance(route, int)) or (not isinstance(_date, date))):
            return None
            
        # Get the vehicle and route objects
        vehicle = BusVehicle.getWithLicencePlate(licensePlate)
        route_obj = Route.getWithNumber(route)
        
        if not vehicle or not route_obj:
            return None
            
        try:
            return self.btms.addAssignment(_date, vehicle, route_obj)
        except RuntimeError:
            # Assignment creation failed
            return None