from datetime import date, timedelta
from assets.BTMS.model.umple import *


class BTMSController:
    def __init__(self):
        self.btms = BTMS()

    def create_driver(self, drivername: str):
        """
        Creates a new driver with the given name.
        The driver name must be a non-empty string.
        """
        if not drivername or not isinstance(drivername, str):
            raise ValueError("Driver name must be a non-empty string")
        
        # Check if driver with this name already exists
        if Driver.hasWithName(drivername):
            raise ValueError(f"Driver with name '{drivername}' already exists")
        
        # Create and add the driver
        self.btms.addDriver1(drivername)
        return f"Driver {drivername} created successfully"

    def create_route(self, number: int):
        """
        Creates a new route with the given number.
        The route number must be an integer between 1 and 9999.
        """
        if not isinstance(number, int) or number < 1 or number > 9999:
            raise ValueError("Route number must be an integer between 1 and 9999")
        
        # Check if route with this number already exists
        if Route.hasWithNumber(number):
            raise ValueError(f"Route with number {number} already exists")
        
        # Create and add the route
        self.btms.addRoute1(number)
        return f"Route {number} created successfully"

    def create_route_assignment(self, licensePlate: str, route: int, _date: date):
        """
        Creates a new route assignment for a bus vehicle on a specific route and date.
        - licensePlate must be a non-empty string
        - route must be an existing route number
        - date must be within one year from today
        """
        # Validate license plate
        if not licensePlate or not isinstance(licensePlate, str):
            raise ValueError("License plate must be a non-empty string")
        
        # Validate route exists
        if not Route.hasWithNumber(route):
            raise ValueError(f"Route {route} does not exist")
        
        # Validate date is within one year from today
        today = date.today()
        one_year_later = today + timedelta(days=365)
        if _date < today or _date > one_year_later:
            raise ValueError("Date must be within one year from today")
        
        # Check if bus vehicle exists, create if not
        if not BusVehicle.hasWithLicencePlate(licensePlate):
            self.btms.addVehicle1(licensePlate)
        
        # Get the bus and route objects
        bus = BusVehicle.getWithLicencePlate(licensePlate)
        route_obj = Route.getWithNumber(route)
        
        # Check if this assignment already exists
        for assignment in self.btms.getAssignments():
            if (assignment.getBus() == bus and 
                assignment.getRoute() == route_obj and 
                assignment.getDate() == _date):
                raise ValueError(f"Assignment for bus {licensePlate} on route {route} for date {_date} already exists")
        
        # Create and add the assignment
        self.btms.addAssignment1(_date, bus, route_obj)
        return f"Assignment created for bus {licensePlate} on route {route} for date {_date}"