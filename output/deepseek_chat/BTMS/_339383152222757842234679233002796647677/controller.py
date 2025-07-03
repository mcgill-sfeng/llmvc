from datetime import date, timedelta
from typing import Optional

from assets.BTMS.model.umple import BTMS


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
            # Assuming BTMS.create_driver returns the driver ID or raises an exception
            driver_id = self.btms.create_driver(drivername)
            return driver_id
        except Exception:
            return None

    def create_route(self, number: int) -> bool:
        """
        Creates a new route in the system.
        
        Args:
            number: Route number (must be between 1 and 9999)
            
        Returns:
            bool: True if route was created successfully, False otherwise
        """
        if not isinstance(number, int) or number < 1 or number > 9999:
            return False
            
        try:
            # Assuming BTMS.create_route returns True/False or raises an exception
            return self.btms.create_route(number)
        except Exception:
            return False

    def create_route_assignment(self, licensePlate: str, route: int, _date: date) -> bool:
        """
        Creates a new route assignment in the system.
        
        Args:
            licensePlate: License plate of the bus (non-empty string)
            route: Route number (must exist in system)
            _date: Date of assignment (must be within 1 year from today)
            
        Returns:
            bool: True if assignment was created successfully, False otherwise
        """
        # Validate license plate
        if not licensePlate or not isinstance(licensePlate, str):
            return False
            
        # Validate date is within 1 year from today
        today = date.today()
        one_year_later = today + timedelta(days=365)
        if not isinstance(_date, date) or _date < today or _date > one_year_later:
            return False
            
        try:
            # Assuming BTMS.create_route_assignment returns True/False or raises an exception
            return self.btms.create_route_assignment(licensePlate, route, _date)
        except Exception:
            return False