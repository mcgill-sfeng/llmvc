from datetime import date, timedelta
from assets.BTMS.model.ecore import *


class BTMSController:
    def __init__(self):
        self.btms = BTMS()

    def create_driver(self, drivername: str):
        if not drivername:
            raise ValueError("The name of a driver cannot be empty.")
        
        # Assuming the BTMS model has a method to add a new driver
        self.btms.drivers.append(Driver(name=drivername))

    def create_route(self, number: int):
        if number <= 0:
            raise ValueError("The number of a route must be greater than zero.")
        if number > 9999:
            raise ValueError("The number of a route cannot be greater than 9999.")
        
        # Check if route with this number already exists
        if any(route.number == number for route in self.btms.routes):
            raise ValueError("A route with this number already exists. Please use a different number.")
        
        # Assuming the BTMS model has a method to add a new route
        self.btms.routes.append(Route(number=number))

    def create_route_assignment(self, licensePlate: str, route: int, _date: date):
        # Validate bus vehicle exists
        bus = next((v for v in self.btms.vehicles if v.licencePlate == licensePlate), None)
        if not bus:
            raise ValueError("A bus must be specified for the assignment.")
        
        # Validate route exists
        route_obj = next((r for r in self.btms.routes if r.number == route), None)
        if not route_obj:
            raise ValueError("A route must be specified for the assignment.")
        
        # Validate date is within one year from today
        today = date.today()
        one_year_later = today + timedelta(days=365)
        if _date < today or _date > one_year_later:
            raise ValueError("The date must be within a year from today.")
        
        # Check if bus is in repair shop (assuming BusVehicle has this attribute)
        if hasattr(bus, 'inRepairShop') and bus.inRepairShop:
            raise ValueError("Cannot assign a bus that's in the repair shop.")
        
        # Create new route assignment
        assignment = RouteAssignment(date=_date, bus=bus, route=route_obj)
        self.btms.assignments.append(assignment)
        bus.assignments.append(assignment)
        route_obj.assignments.append(assignment)