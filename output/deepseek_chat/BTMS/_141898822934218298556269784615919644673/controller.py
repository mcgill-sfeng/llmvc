from datetime import date, timedelta
from assets.BTMS.model.umple import *


class BTMSController:
    def __init__(self):
        self.btms = BTMS()

    def create_driver(self, drivername: str):
        """
        Creates a new driver with the given name.
        
        Args:
            drivername: The name of the driver to create (must be unique)
            
        Returns:
            The created Driver object
            
        Raises:
            ValueError: If a driver with the same name already exists
        """
        if not drivername:
            raise ValueError("Driver name cannot be empty")
            
        if Driver.hasWithName(drivername):
            raise ValueError(f"Driver with name '{drivername}' already exists")
            
        return self.btms.addDriver(drivername)

    def create_route(self, number: int):
        """
        Creates a new route with the given number.
        
        Args:
            number: The route number (must be between 1-9999 and unique)
            
        Returns:
            The created Route object
            
        Raises:
            ValueError: If the route number is invalid or already exists
        """
        if not (1 <= number <= 9999):
            raise ValueError("Route number must be between 1 and 9999")
            
        if Route.hasWithNumber(number):
            raise ValueError(f"Route with number {number} already exists")
            
        return self.btms.addRoute(number)

    def create_route_assignment(self, licensePlate: str, route: int, _date: date):
        """
        Creates a new route assignment for a bus on a specific date.
        
        Args:
            licensePlate: The license plate of the bus
            route: The route number
            _date: The date of the assignment (must be within 1 year from today)
            
        Returns:
            The created RouteAssignment object
            
        Raises:
            ValueError: If any parameter is invalid or constraints are violated
        """
        # Validate date is within 1 year from today
        today = date.today()
        one_year_later = today + timedelta(days=365)
        
        if _date < today or _date > one_year_later:
            raise ValueError("Assignment date must be within 1 year from today")
            
        # Check if bus exists
        bus = BusVehicle.getWithLicencePlate(licensePlate)
        if not bus:
            raise ValueError(f"Bus with license plate '{licensePlate}' does not exist")
            
        # Check if route exists
        route_obj = Route.getWithNumber(route)
        if not route_obj:
            raise ValueError(f"Route with number {route} does not exist")
            
        # Check if assignment already exists for this bus on this date
        for assignment in self.btms.getAssignments():
            if (assignment.getBus() == bus and 
                assignment.getDate() == _date):
                raise ValueError(f"Bus {licensePlate} is already assigned on {_date}")
                
        # Check if assignment already exists for this route on this date
        for assignment in self.btms.getAssignments():
            if (assignment.getRoute() == route_obj and 
                assignment.getDate() == _date):
                raise ValueError(f"Route {route} is already assigned on {_date}")
                
        return self.btms.addAssignment(_date, bus, route_obj)