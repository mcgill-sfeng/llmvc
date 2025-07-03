from datetime import date, timedelta
from assets.BTMS.model.ecore import *

class BTMSController:
    def __init__(self):
        self.btms = BTMS(vehicles=[], routes=[], assignments=[], drivers=[], schedules=[])

    def create_driver(self, drivername: str):
        # Check if the driver name is valid
        if not drivername or not isinstance(drivername, str):
            raise ValueError("Driver name must be a non-empty string.")
        
        # Create a new Driver instance
        new_driver = Driver(name=drivername, schedules=[])
        
        # Add the new driver to the BTMS
        self.btms.drivers.append(new_driver)

    def create_route(self, number: int):
        # Check if the route number is valid
        if not (1 <= number <= 9999):
            raise ValueError("Route number must be an integer between 1 and 9999.")
        
        # Create a new Route instance
        new_route = Route(number=number, assignments=[])
        
        # Add the new route to the BTMS
        self.btms.routes.append(new_route)

    def create_route_assignment(self, licensePlate: str, route: int, _date: date):
        # Check if the date is valid (within one year from today)
        today = date.today()
        if not (today <= _date <= today + timedelta(days=365)):
            raise ValueError("Date must be within one year from today.")
        
        # Find the bus vehicle by license plate
        bus = next((vehicle for vehicle in self.btms.vehicles if vehicle.licencePlate == licensePlate), None)
        if bus is None:
            raise ValueError("Bus vehicle with the given license plate does not exist.")
        
        # Find the route by number
        route_obj = next((r for r in self.btms.routes if r.number == route), None)
        if route_obj is None:
            raise ValueError("Route with the given number does not exist.")
        
        # Create a new RouteAssignment instance
        new_assignment = RouteAssignment(date=_date, bus=bus, route=route_obj, schedules=[])
        
        # Add the new assignment to the BTMS
        self.btms.assignments.append(new_assignment)
        bus.assignments.append(new_assignment)
        route_obj.assignments.append(new_assignment)