from datetime import date, timedelta
from typing import Optional
from assets.BTMS.model.ecore import *


class BTMSController:
    def __init__(self):
        self.btms = BTMS()

    def create_driver(self, drivername: str) -> Optional[str]:
        """
        Creates a new driver in the system.
        
        Args:
            drivername: Name of the driver to create
            
        Returns:
            str: The generated driver ID if successful, None otherwise
        """
        if not drivername or not isinstance(drivername, str):
            return None
            
        try:
            # Assuming BTMS model has a method to create drivers
            driver_id = self.btms.create_driver(drivername)
            return driver_id
        except Exception:
            return None

    def create_route(self, number: int) -> Optional[int]:
        """
        Creates a new route in the system.
        
        Args:
            number: Route number (must be between 1 and 9999)
            
        Returns:
            int: The route number if successful, None otherwise
        """
        if not isinstance(number, int) or number < 1 or number > 9999:
            return None
            
        try:
            # Assuming BTMS model has a method to create routes
            route_number = self.btms.create_route(number)
            return route_number
        except Exception:
            return None

    def create_route_assignment(self, licensePlate: str, route: int, _date: date) -> Optional[str]:
        """
        Creates a new route assignment in the system.
        
        Args:
            licensePlate: License plate of the bus (non-empty string)
            route: Route number (must exist in system)
            _date: Date of assignment (must be within 1 year from today)
            
        Returns:
            str: Assignment ID if successful, None otherwise
        """
        # Validate license plate
        if not licensePlate or not isinstance(licensePlate, str):
            return None
            
        # Validate route number
        if not isinstance(route, int) or route < 1 or route > 9999:
            return None
            
        # Validate date
        today = date.today()
        one_year_later = today + timedelta(days=365)
        if not isinstance(_date, date) or _date < today or _date > one_year_later:
            return None
            
        try:
            # Check if bus and route exist in system
            # Assuming BTMS has methods to check existence
            if not self.btms.bus_exists(licensePlate) or not self.btms.route_exists(route):
                return None
                
            # Create the assignment
            assignment_id = self.btms.create_route_assignment(licensePlate, route, _date)
            return assignment_id
        except Exception:
            return None