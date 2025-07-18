from datetime import date, timedelta
from assets.BTMS.model.umple import *

class BTMSController:
    def __init__(self):
        self.btms = BTMS()

    def create_driver(self, drivername: str):
        if not drivername:
            raise ValueError("Driver name cannot be empty.")
        
        # Check if the driver already exists
        for driver in self.btms.drivers:
            if driver.name == drivername:
                raise ValueError("Driver with this name already exists.")
        
        # Create and add the new driver
        new_driver = Driver(name=drivername)
        self.btms.drivers.append(new_driver)

    def create_route(self, number: int):
        if number < 1 or number > 9999:
            raise ValueError("Route number must be between 1 and 9999.")
        
        # Check if the route already exists
        for route in self.btms.routes:
            if route.number == number:
                raise ValueError("Route with this number already exists.")
        
        # Create and add the new route
        new_route = Route(number=number)
        self.btms.routes.append(new_route)

    def create_route_assignment(self, licensePlate: str, route: int, _date: date):
        if not licensePlate:
            raise ValueError("License plate cannot be empty.")
        
        # Check if the bus vehicle exists
        bus_vehicle = next((bv for bv in self.btms.vehicles if bv.licencePlate == licensePlate), None)
        if bus_vehicle is None:
            raise ValueError("Bus vehicle with this license plate does not exist.")
        
        # Check if the route exists
        route_obj = next((r for r in self.btms.routes if r.number == route), None)
        if route_obj is None:
            raise ValueError("Route with this number does not exist.")
        
        # Check if the date is valid (within one year from today)
        today = date.today()
        if _date < today or _date > today + timedelta(days=365):
            raise ValueError("Date must be within one year from today.")
        
        # Create and add the new route assignment
        new_assignment = RouteAssignment(date=_date)
        new_assignment.bus = bus_vehicle
        new_assignment.route = route_obj
        self.btms.assignments.append(new_assignment)