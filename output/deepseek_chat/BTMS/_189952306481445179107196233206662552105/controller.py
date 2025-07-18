from datetime import date, timedelta
from typing import Optional
from enum import Enum
from assets.BTMS.model.ecore import *

class Shift(Enum):
    MORNING = "Morning"
    AFTERNOON = "Afternoon"
    NIGHT = "Night"

class BTMSController:
    def __init__(self):
        self.btms = BTMS()

    def create_driver(self, drivername: str):
        """Creates a new driver with the given name.
        
        Args:
            drivername: The name of the driver to create.
            
        Returns:
            The created Driver object.
            
        Raises:
            ValueError: If drivername is empty or None.
        """
        if not drivername:
            raise ValueError("Driver name cannot be empty")
            
        driver = Driver()
        driver.name = drivername
        self.btms.drivers.append(driver)
        return driver

    def create_route(self, number: int):
        """Creates a new route with the given number.
        
        Args:
            number: The route number (must be between 1 and 9999).
            
        Returns:
            The created Route object.
            
        Raises:
            ValueError: If route number is invalid.
        """
        if number < 1 or number > 9999:
            raise ValueError("Route number must be between 1 and 9999")
            
        # Check if route already exists
        if any(r.number == number for r in self.btms.routes):
            raise ValueError(f"Route with number {number} already exists")
            
        route = Route()
        route.number = number
        self.btms.routes.append(route)
        return route

    def create_route_assignment(self, licensePlate: str, route: int, _date: date):
        """Creates a new route assignment.
        
        Args:
            licensePlate: The license plate of the bus vehicle.
            route: The route number to assign.
            _date: The date of the assignment (must be within 1 year from today).
            
        Returns:
            The created RouteAssignment object.
            
        Raises:
            ValueError: If any parameter is invalid or constraints are violated.
        """
        # Validate date
        today = date.today()
        one_year_later = today + timedelta(days=365)
        if _date < today or _date > one_year_later:
            raise ValueError("Date must be within one year from today")
            
        # Find bus vehicle
        bus = next((v for v in self.btms.vehicles if v.licencePlate == licensePlate), None)
        if not bus:
            raise ValueError(f"Bus with license plate {licensePlate} not found")
            
        # Find route
        route_obj = next((r for r in self.btms.routes if r.number == route), None)
        if not route_obj:
            raise ValueError(f"Route with number {route} not found")
            
        # Check if assignment already exists for this bus on this date
        if any(ra for ra in bus.assignments if ra.date == _date):
            raise ValueError(f"Bus {licensePlate} already has an assignment on {_date}")
            
        # Create the assignment
        assignment = RouteAssignment()
        assignment.date = _date
        assignment.bus = bus
        assignment.route = route_obj
        
        # Add to collections
        bus.assignments.append(assignment)
        route_obj.assignments.append(assignment)
        self.btms.assignments.append(assignment)
        
        return assignment