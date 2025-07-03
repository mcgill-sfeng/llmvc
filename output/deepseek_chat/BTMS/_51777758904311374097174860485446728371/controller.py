from datetime import date
from assets.BTMS.model.ecore import *


class BTMSController:
    def __init__(self):
        self.btms = BTMS(vehicles=[], routes=[], assignments=[], drivers=[], schedules=[])

    def create_driver(self, drivername: str):
        """Creates a new driver with the given name and adds it to the BTMS system.
        
        Args:
            drivername: The name of the driver to create.
        """
        driver = Driver(name=drivername, schedules=[])
        self.btms.drivers.append(driver)
        return driver

    def create_route(self, number: int):
        """Creates a new route with the given number and adds it to the BTMS system.
        
        Args:
            number: The route number to create.
        """
        route = Route(number=number, assignments=[])
        self.btms.routes.append(route)
        return route

    def create_route_assignment(self, licensePlate: str, route: int, _date: date):
        """Creates a new route assignment linking a bus vehicle to a route on a specific date.
        
        Args:
            licensePlate: The license plate of the bus vehicle.
            route: The route number to assign.
            _date: The date of the assignment.
            
        Returns:
            The created RouteAssignment object.
            
        Raises:
            ValueError: If the bus vehicle or route doesn't exist.
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
        assignment = RouteAssignment(date=_date, bus=bus, route=route_obj, schedules=[])
        
        # Update references
        bus.assignments.append(assignment)
        route_obj.assignments.append(assignment)
        self.btms.assignments.append(assignment)
        
        return assignment