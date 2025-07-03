from datetime import date, timedelta
from assets.BTMS.model.umple import *


class BTMSController:
    def __init__(self):
        self.btms = BTMS()

    def create_driver(self, drivername: str):
        """
        Creates a new driver with the given name.
        Raises ValueError if driver name is empty or already exists.
        """
        if not drivername:
            raise ValueError("Driver name cannot be empty")
        
        if Driver.hasWithName(drivername):
            raise ValueError(f"Driver with name '{drivername}' already exists")
            
        return self.btms.addDriver1(drivername)

    def create_route(self, number: int):
        """
        Creates a new route with the given number.
        Raises ValueError if route number is invalid or already exists.
        """
        if number < 1 or number > 9999:
            raise ValueError("Route number must be between 1 and 9999")
            
        if Route.hasWithNumber(number):
            raise ValueError(f"Route with number {number} already exists")
            
        return self.btms.addRoute1(number)

    def create_route_assignment(self, licensePlate: str, route: int, _date: date):
        """
        Creates a new route assignment for the given bus, route, and date.
        Raises ValueError if any parameter is invalid or constraints are violated.
        """
        # Validate date is within one year from today
        today = date.today()
        one_year_later = today + timedelta(days=365)
        
        if _date < today or _date > one_year_later:
            raise ValueError("Date must be within one year from today")
            
        # Check if bus exists
        if not BusVehicle.hasWithLicencePlate(licensePlate):
            raise ValueError(f"Bus with license plate '{licensePlate}' does not exist")
            
        # Check if route exists
        if not Route.hasWithNumber(route):
            raise ValueError(f"Route with number {route} does not exist")
            
        # Get the bus and route objects
        bus = BusVehicle.getWithLicencePlate(licensePlate)
        route_obj = Route.getWithNumber(route)
        
        # Check if assignment already exists for this bus on this date
        for assignment in self.btms.getAssignments():
            if assignment.getBus() == bus and assignment.getDate() == _date:
                raise ValueError(f"Bus {licensePlate} already has an assignment on {_date}")
                
        # Create the new assignment
        return self.btms.addAssignment1(_date, bus, route_obj)