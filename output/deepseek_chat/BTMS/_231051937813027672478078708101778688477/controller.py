from datetime import date
from assets.BTMS.model.ecore import *


class BTMSController:
    def __init__(self):
        self.btms = BTMS()

    def create_driver(self, drivername: str):
        """Creates a new driver and adds it to the BTMS system.
        
        Args:
            drivername: The name of the driver to create.
            
        Returns:
            The created Driver object.
        """
        driver = Driver()
        driver.name = drivername
        self.btms.drivers.append(driver)
        return driver

    def create_route(self, number: int):
        """Creates a new route and adds it to the BTMS system.
        
        Args:
            number: The route number to create.
            
        Returns:
            The created Route object.
        """
        route = Route()
        route.number = number
        self.btms.routes.append(route)
        return route

    def create_route_assignment(self, licensePlate: str, route: int, _date: date):
        """Creates a new route assignment and links it to the appropriate bus and route.
        
        Args:
            licensePlate: The license plate of the bus to assign.
            route: The route number to assign the bus to.
            _date: The date for the assignment.
            
        Returns:
            The created RouteAssignment object.
            
        Raises:
            ValueError: If bus or route is not found.
        """
        # Find the bus vehicle
        bus = next((v for v in self.btms.vehicles if v.licencePlate == licensePlate), None)
        if not bus:
            raise ValueError(f"Bus with license plate {licensePlate} not found")
            
        # Find the route
        route_obj = next((r for r in self.btms.routes if r.number == route), None)
        if not route_obj:
            raise ValueError(f"Route {route} not found")
            
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