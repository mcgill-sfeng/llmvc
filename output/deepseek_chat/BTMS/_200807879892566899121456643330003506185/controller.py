from datetime import date
from assets.BTMS.model.umple import *


class BTMSController:
    def __init__(self):
        self.btms = BTMS()

    def create_driver(self, drivername: str):
        """
        Creates a new driver in the system.
        
        Args:
            drivername: The name of the driver to create
            
        Returns:
            The created driver object or None if creation failed
        """
        if not drivername or not isinstance(drivername, str):
            raise ValueError("Driver name must be a non-empty string")
        
        try:
            return self.btms.create_driver(drivername)
        except Exception as e:
            # Log the error in a real system
            raise RuntimeError(f"Failed to create driver: {str(e)}")

    def create_route(self, number: int):
        """
        Creates a new route in the system.
        
        Args:
            number: The route number to create
            
        Returns:
            The created route object or None if creation failed
        """
        if not isinstance(number, int) or number <= 0:
            raise ValueError("Route number must be a positive integer")
            
        try:
            return self.btms.create_route(number)
        except Exception as e:
            # Log the error in a real system
            raise RuntimeError(f"Failed to create route: {str(e)}")

    def create_route_assignment(self, licensePlate: str, route: int, _date: date):
        """
        Creates a new route assignment in the system.
        
        Args:
            licensePlate: The vehicle license plate
            route: The route number
            _date: The date of the assignment
            
        Returns:
            The created route assignment object or None if creation failed
        """
        if not licensePlate or not isinstance(licensePlate, str):
            raise ValueError("License plate must be a non-empty string")
        if not isinstance(route, int) or route <= 0:
            raise ValueError("Route must be a positive integer")
        if not isinstance(_date, date):
            raise ValueError("Date must be a datetime.date object")
            
        try:
            return self.btms.create_route_assignment(licensePlate, route, _date)
        except Exception as e:
            # Log the error in a real system
            raise RuntimeError(f"Failed to create route assignment: {str(e)}")