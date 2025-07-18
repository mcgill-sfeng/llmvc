from datetime import date
from assets.BTMS.model.umple import *


class BTMSController:
    def __init__(self):
        self.btms = BTMS()

    def create_driver(self, drivername: str):
        """Creates a new driver with the given name.
        
        Args:
            drivername: The name of the driver to create.
            
        Returns:
            The created Driver object.
        """
        # Check if driver already exists
        for driver in self.btms.getDrivers():
            if driver.getName() == drivername:
                raise ValueError(f"Driver with name '{drivername}' already exists")
        
        # Create new driver
        new_driver = self.btms.addDriver()
        new_driver.setName(drivername)
        return new_driver

    def create_route(self, number: int):
        """Creates a new route with the given number.
        
        Args:
            number: The route number to create.
            
        Returns:
            The created Route object.
        """
        # Check if route already exists
        for route in self.btms.getRoutes():
            if route.getNumber() == number:
                raise ValueError(f"Route with number {number} already exists")
        
        # Create new route
        new_route = self.btms.addRoute()
        new_route.setNumber(number)
        return new_route

    def create_route_assignment(self, licensePlate: str, route: int, _date: date):
        """Creates a new route assignment.
        
        Args:
            licensePlate: The license plate of the bus vehicle.
            route: The route number to assign.
            _date: The date for the assignment.
            
        Returns:
            The created RouteAssignment object.
        """
        # Find the bus vehicle
        bus = None
        for vehicle in self.btms.getVehicles():
            if vehicle.getLicencePlate() == licensePlate:
                bus = vehicle
                break
        if not bus:
            raise ValueError(f"Bus with license plate '{licensePlate}' not found")
        
        # Find the route
        route_obj = None
        for r in self.btms.getRoutes():
            if r.getNumber() == route:
                route_obj = r
                break
        if not route_obj:
            raise ValueError(f"Route with number {route} not found")
        
        # Check for existing assignment on the same date
        for assignment in self.btms.getAssignments():
            if (assignment.getBus() == bus and 
                assignment.getRoute() == route_obj and 
                assignment.getDate() == _date):
                raise ValueError(f"Assignment already exists for this bus, route, and date")
        
        # Create new assignment
        new_assignment = self.btms.addAssignment()
        new_assignment.setBus(bus)
        new_assignment.setRoute(route_obj)
        new_assignment.setDate(_date)
        return new_assignment