from datetime import date
from assets.BTMS.model.ecore import *


class BTMSController:
    def __init__(self):
        self.btms = BTMS()

    def create_driver(self, drivername: str):
        """Creates a new driver in the BTMS system.
        
        Args:
            drivername: The name of the driver to create (must be non-empty string)
            
        Returns:
            The created driver object
            
        Raises:
            ValueError: If drivername is empty or not a string
        """
        if not isinstance(drivername, str) or not drivername.strip():
            raise ValueError("Driver name must be a non-empty string")
        return self.btms.create_driver(drivername)

    def create_route(self, number: int):
        """Creates a new route in the BTMS system.
        
        Args:
            number: The route number (must be positive integer)
            
        Returns:
            The created route object
            
        Raises:
            ValueError: If number is not a positive integer
        """
        if not isinstance(number, int) or number <= 0:
            raise ValueError("Route number must be a positive integer")
        return self.btms.create_route(number)

    def create_route_assignment(self, licensePlate: str, route: int, _date: date):
        """Creates a new route assignment in the BTMS system.
        
        Args:
            licensePlate: Vehicle license plate (must be non-empty string)
            route: Route number (must be positive integer)
            _date: Date of assignment (must be date object)
            
        Returns:
            The created route assignment object
            
        Raises:
            ValueError: If any parameter is invalid
            TypeError: If _date is not a date object
        """
        if not isinstance(licensePlate, str) or not licensePlate.strip():
            raise ValueError("License plate must be a non-empty string")
        if not isinstance(route, int) or route <= 0:
            raise ValueError("Route number must be a positive integer")
        if not isinstance(_date, date):
            raise TypeError("Date must be a datetime.date object")
            
        return self.btms.create_route_assignment(licensePlate, route, _date)