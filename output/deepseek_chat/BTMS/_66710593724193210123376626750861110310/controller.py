from datetime import date, timedelta
from typing import Optional
from assets.BTMS.model.umple import *


class BTMSController:
    def __init__(self):
        self.btms = BTMS()

    def create_driver(self, drivername: str) -> Optional[Driver]:
        """Create a new driver with the given name.
        
        Args:
            drivername: Name of the driver to create
            
        Returns:
            The created Driver object if successful, None if driver already exists
        """
        if not drivername:
            return None
            
        # Check if driver with this name already exists
        existing_driver = next((d for d in self.btms.drivers if d.name == drivername), None)
        if existing_driver:
            return None
            
        new_driver = Driver()
        new_driver.name = drivername
        self.btms.drivers.append(new_driver)
        return new_driver

    def create_route(self, number: int) -> Optional[Route]:
        """Create a new route with the given number.
        
        Args:
            number: Route number (must be between 1 and 9999)
            
        Returns:
            The created Route object if successful, None if invalid number or route exists
        """
        if number < 1 or number > 9999:
            return None
            
        # Check if route with this number already exists
        existing_route = next((r for r in self.btms.routes if r.number == number), None)
        if existing_route:
            return None
            
        new_route = Route()
        new_route.number = number
        self.btms.routes.append(new_route)
        return new_route

    def create_route_assignment(self, licensePlate: str, route: int, _date: date) -> Optional[RouteAssignment]:
        """Create a new route assignment.
        
        Args:
            licensePlate: License plate of the bus vehicle
            route: Route number
            _date: Date of assignment (must be within 1 year from today)
            
        Returns:
            The created RouteAssignment object if successful, None if invalid parameters
        """
        if not licensePlate:
            return None
            
        # Validate date is within 1 year from today
        today = date.today()
        one_year_later = today + timedelta(days=365)
        if _date < today or _date > one_year_later:
            return None
            
        # Check if bus vehicle exists
        bus = next((v for v in self.btms.vehicles if v.licencePlate == licensePlate), None)
        if not bus:
            return None
            
        # Check if route exists
        route_obj = next((r for r in self.btms.routes if r.number == route), None)
        if not route_obj:
            return None
            
        # Check if assignment already exists for this bus on this date
        existing_assignment = next(
            (a for a in self.btms.assignments 
             if a.bus == bus and a.date == _date),
            None
        )
        if existing_assignment:
            return None
            
        new_assignment = RouteAssignment()
        new_assignment.date = _date
        new_assignment.bus = bus
        new_assignment.route = route_obj
        self.btms.assignments.append(new_assignment)
        return new_assignment