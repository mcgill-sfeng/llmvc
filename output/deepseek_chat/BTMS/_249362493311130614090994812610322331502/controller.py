from datetime import date, timedelta
from typing import Optional
from assets.BTMS.model.ecore import *


class BTMSController:
    def __init__(self):
        self.btms = BTMS()

    def create_driver(self, drivername: str):
        """Creates a new driver with the given name.
        
        Args:
            drivername: The name of the driver to create
            
        Returns:
            The created Driver object
            
        Raises:
            ValueError: If the driver name is empty or already exists
        """
        if not drivername:
            raise ValueError("Driver name cannot be empty")
            
        # Check if driver with this name already exists
        if any(d.name == drivername for d in self.btms.drivers):
            raise ValueError(f"Driver with name '{drivername}' already exists")
            
        driver = Driver(name=drivername)
        self.btms.drivers.append(driver)
        return driver

    def create_route(self, number: int):
        """Creates a new route with the given number.
        
        Args:
            number: The route number (must be between 1 and 9999)
            
        Returns:
            The created Route object
            
        Raises:
            ValueError: If the route number is invalid or already exists
        """
        if number < 1 or number > 9999:
            raise ValueError("Route number must be between 1 and 9999")
            
        # Check if route with this number already exists
        if any(r.number == number for r in self.btms.routes):
            raise ValueError(f"Route with number {number} already exists")
            
        route = Route(number=number)
        self.btms.routes.append(route)
        return route

    def create_route_assignment(self, licensePlate: str, route: int, _date: date):
        """Creates a new route assignment for a bus vehicle on a specific date.
        
        Args:
            licensePlate: The license plate of the bus vehicle
            route: The route number to assign
            _date: The date of the assignment (must be within 1 year from today)
            
        Returns:
            The created RouteAssignment object
            
        Raises:
            ValueError: If any of the parameters are invalid or constraints are violated
        """
        if not licensePlate:
            raise ValueError("License plate cannot be empty")
            
        # Validate date is within 1 year from today
        today = date.today()
        one_year_later = today + timedelta(days=365)
        if _date < today or _date > one_year_later:
            raise ValueError("Date must be within one year from today")
            
        # Find the bus vehicle
        bus_vehicle: Optional[BusVehicle] = None
        for bv in self.btms.vehicles:
            if bv.licencePlate == licensePlate:
                bus_vehicle = bv
                break
                
        if not bus_vehicle:
            raise ValueError(f"Bus vehicle with license plate '{licensePlate}' not found")
            
        # Find the route
        route_obj: Optional[Route] = None
        for r in self.btms.routes:
            if r.number == route:
                route_obj = r
                break
                
        if not route_obj:
            raise ValueError(f"Route with number {route} not found")
            
        # Check if this bus is already assigned to any route on this date
        for assignment in self.btms.assignments:
            if assignment.bus == bus_vehicle and assignment.date == _date:
                raise ValueError(f"Bus '{licensePlate}' is already assigned to another route on {_date}")
                
        # Check if this route already has an assignment on this date
        for assignment in self.btms.assignments:
            if assignment.route == route_obj and assignment.date == _date:
                raise ValueError(f"Route {route} already has an assignment on {_date}")
                
        # Create the new assignment
        assignment = RouteAssignment(date=_date, bus=bus_vehicle, route=route_obj)
        self.btms.assignments.append(assignment)
        
        # Update references
        bus_vehicle.assignments.append(assignment)
        route_obj.assignments.append(assignment)
        
        return assignment