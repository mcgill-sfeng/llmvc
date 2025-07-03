from datetime import date, timedelta
from assets.BTMS.model.ecore import *


class BTMSController:
    def __init__(self):
        self.btms = BTMS(vehicles=[], routes=[], assignments=[], drivers=[], schedules=[])

    def create_driver(self, drivername: str):
        """Creates a new driver with the given name.
        
        Args:
            drivername: The name of the driver to create (non-empty string)
            
        Returns:
            The created Driver object
            
        Raises:
            ValueError: If drivername is empty
        """
        if not drivername:
            raise ValueError("Driver name cannot be empty")
        
        # Check if driver with this name already exists
        for driver in self.btms.drivers:
            if driver.name == drivername:
                return driver
                
        new_driver = Driver(name=drivername, schedules=[])
        self.btms.drivers.append(new_driver)
        return new_driver

    def create_route(self, number: int):
        """Creates a new route with the given number.
        
        Args:
            number: The route number (must be between 1 and 9999)
            
        Returns:
            The created Route object
            
        Raises:
            ValueError: If number is not between 1 and 9999
        """
        if number < 1 or number > 9999:
            raise ValueError("Route number must be between 1 and 9999")
            
        # Check if route with this number already exists
        for route in self.btms.routes:
            if route.number == number:
                return route
                
        new_route = Route(number=number, assignments=[])
        self.btms.routes.append(new_route)
        return new_route

    def create_route_assignment(self, licensePlate: str, route: int, _date: date):
        """Creates a new route assignment for a bus vehicle on a specific route and date.
        
        Args:
            licensePlate: The license plate of the bus vehicle (non-empty string)
            route: The route number (must exist in the system)
            _date: The date of the assignment (must be within one year from today)
            
        Returns:
            The created RouteAssignment object
            
        Raises:
            ValueError: If any parameter is invalid or if the assignment already exists
        """
        if not licensePlate:
            raise ValueError("License plate cannot be empty")
            
        # Validate date is within one year from today
        today = date.today()
        one_year_later = today + timedelta(days=365)
        if _date < today or _date > one_year_later:
            raise ValueError("Date must be within one year from today")
            
        # Find the bus vehicle or create it if it doesn't exist
        bus = None
        for vehicle in self.btms.vehicles:
            if vehicle.licencePlate == licensePlate:
                bus = vehicle
                break
                
        if not bus:
            bus = BusVehicle(licencePlate=licensePlate, assignments=[])
            self.btms.vehicles.append(bus)
            
        # Find the route (must exist)
        route_obj = None
        for r in self.btms.routes:
            if r.number == route:
                route_obj = r
                break
                
        if not route_obj:
            raise ValueError(f"Route {route} does not exist")
            
        # Check if assignment already exists for this bus, route, and date
        for assignment in self.btms.assignments:
            if (assignment.bus == bus and 
                assignment.route == route_obj and 
                assignment.date == _date):
                raise ValueError("Route assignment already exists for this bus, route, and date")
                
        # Create new assignment
        new_assignment = RouteAssignment(date=_date, bus=bus, route=route_obj, schedules=[])
        self.btms.assignments.append(new_assignment)
        bus.assignments.append(new_assignment)
        route_obj.assignments.append(new_assignment)
        
        return new_assignment