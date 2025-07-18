from datetime import date
from assets.BTMS.model.ecore import *
from assets.BTMS.model.ecore import *


class BTMSController:
    def __init__(self):
        self.btms = BTMS()

    def create_driver(self, drivername: str):
        """Creates a new driver with the given name and adds it to the BTMS system.
        
        Args:
            drivername: The name of the driver to create
            
        Returns:
            The created Driver object
        """
        # Check if driver with this name already exists
        if any(d.name == drivername for d in self.btms.drivers):
            raise ValueError(f"Driver with name '{drivername}' already exists")
            
        driver = Driver(name=drivername)
        self.btms.drivers.append(driver)
        return driver

    def create_route(self, number: int):
        """Creates a new route with the given number and adds it to the BTMS system.
        
        Args:
            number: The route number to create
            
        Returns:
            The created Route object
        """
        # Check if route with this number already exists
        if any(r.number == number for r in self.btms.routes):
            raise ValueError(f"Route with number {number} already exists")
            
        route = Route(number=number)
        self.btms.routes.append(route)
        return route

    def create_route_assignment(self, licensePlate: str, route: int, _date: date):
        """Creates a new route assignment for a bus on a specific date.
        
        Args:
            licensePlate: The license plate of the bus
            route: The route number to assign
            _date: The date of the assignment
            
        Returns:
            The created RouteAssignment object
            
        Raises:
            ValueError: If bus or route doesn't exist, or if assignment already exists
        """
        # Find the bus
        bus = next((v for v in self.btms.vehicles if v.licencePlate == licensePlate), None)
        if not bus:
            raise ValueError(f"Bus with license plate '{licensePlate}' not found")
            
        # Find the route
        route_obj = next((r for r in self.btms.routes if r.number == route), None)
        if not route_obj:
            raise ValueError(f"Route with number {route} not found")
            
        # Check if assignment already exists for this bus on this date
        if any(a for a in self.btms.assignments 
               if a.bus == bus and a.date == _date):
            raise ValueError(f"Assignment already exists for bus {licensePlate} on {_date}")
            
        # Check if assignment already exists for this route on this date
        if any(a for a in self.btms.assignments 
               if a.route == route_obj and a.date == _date):
            raise ValueError(f"Assignment already exists for route {route} on {_date}")
            
        # Create the assignment
        assignment = RouteAssignment(date=_date, bus=bus, route=route_obj)
        self.btms.assignments.append(assignment)
        
        # Update references
        bus.assignments.append(assignment)
        route_obj.assignments.append(assignment)
        
        return assignment