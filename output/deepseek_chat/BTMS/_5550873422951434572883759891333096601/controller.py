from datetime import date, timedelta
from assets.BTMS.model.ecore import *


class BTMSController:
    def __init__(self):
        self.btms = BTMS(vehicles=[], routes=[], assignments=[], drivers=[], schedules=[])

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
            
        # Check if driver with same name already exists (assuming names must be unique)
        for driver in self.btms.drivers:
            if driver.name == drivername:
                raise ValueError(f"Driver with name '{drivername}' already exists")
                
        new_driver = Driver(name=drivername, schedules=[])
        self.btms.drivers.append(new_driver)
        return new_driver

    def create_route(self, number: int):
        """Creates a new route with the given number.
        
        Args:
            number: The route number (must be between 1 and 9999).
            
        Returns:
            The created Route object.
            
        Raises:
            ValueError: If number is outside valid range or route already exists.
        """
        if number < 1 or number > 9999:
            raise ValueError("Route number must be between 1 and 9999")
            
        # Check if route with same number already exists
        for route in self.btms.routes:
            if route.number == number:
                raise ValueError(f"Route with number {number} already exists")
                
        new_route = Route(number=number, assignments=[])
        self.btms.routes.append(new_route)
        return new_route

    def create_route_assignment(self, licensePlate: str, route: int, _date: date):
        """Creates a new route assignment for a bus on a specific route and date.
        
        Args:
            licensePlate: The license plate of the bus.
            route: The route number.
            _date: The date of the assignment (must be within 1 year from today).
            
        Returns:
            The created RouteAssignment object.
            
        Raises:
            ValueError: If any parameter is invalid or constraints are violated.
        """
        if not licensePlate:
            raise ValueError("License plate cannot be empty")
            
        # Check date is within 1 year from today
        today = date.today()
        one_year_later = today + timedelta(days=365)
        if _date < today or _date > one_year_later:
            raise ValueError("Date must be within one year from today")
            
        # Find the bus vehicle
        bus_vehicle = None
        for vehicle in self.btms.vehicles:
            if vehicle.licencePlate == licensePlate:
                bus_vehicle = vehicle
                break
                
        if not bus_vehicle:
            raise ValueError(f"Bus with license plate '{licensePlate}' not found")
            
        # Find the route
        route_obj = None
        for r in self.btms.routes:
            if r.number == route:
                route_obj = r
                break
                
        if not route_obj:
            raise ValueError(f"Route with number {route} not found")
            
        # Check if this bus is already assigned to any route on this date
        for assignment in self.btms.assignments:
            if assignment.bus == bus_vehicle and assignment.date == _date:
                raise ValueError(f"Bus {licensePlate} is already assigned to another route on {_date}")
                
        # Create the new assignment
        new_assignment = RouteAssignment(
            date=_date,
            bus=bus_vehicle,
            route=route_obj,
            schedules=[]
        )
        
        # Update references
        bus_vehicle.assignments.append(new_assignment)
        route_obj.assignments.append(new_assignment)
        self.btms.assignments.append(new_assignment)
        
        return new_assignment