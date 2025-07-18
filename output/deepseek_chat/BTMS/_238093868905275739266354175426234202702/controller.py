from datetime import date, timedelta
from assets.BTMS.model.ecore import *


class BTMSController:
    def __init__(self):
        self.btms = BTMS(vehicles=[], routes=[], assignments=[], drivers=[], schedules=[])

    def create_driver(self, drivername: str):
        if not drivername:
            raise ValueError("The name of a driver cannot be empty.")
        
        new_driver = Driver(name=drivername, schedules=[])
        self.btms.drivers.append(new_driver)
        return new_driver

    def create_route(self, number: int):
        if number <= 0:
            raise ValueError("The number of a route must be greater than zero.")
        if number > 9999:
            raise ValueError("The number of a route cannot be greater than 9999.")
        
        if any(route.number == number for route in self.btms.routes):
            raise ValueError("A route with this number already exists. Please use a different number.")
        
        new_route = Route(number=number, assignments=[])
        self.btms.routes.append(new_route)
        return new_route

    def create_route_assignment(self, licensePlate: str, route: int, _date: date):
        # Validate bus vehicle exists
        bus_vehicle = next((v for v in self.btms.vehicles if v.licencePlate == licensePlate), None)
        if not bus_vehicle:
            raise ValueError("A bus must be specified for the assignment.")
        
        # Validate route exists
        route_obj = next((r for r in self.btms.routes if r.number == route), None)
        if not route_obj:
            raise ValueError("A route must be specified for the assignment.")
        
        # Validate date is within one year from today
        today = date(2021, 10, 7)  # As specified in the background
        one_year_later = today + timedelta(days=365)
        if _date < today or _date > one_year_later:
            raise ValueError("The date must be within a year from today.")
        
        # Check if bus is in repair shop (if this information is available)
        if hasattr(bus_vehicle, 'inRepairShop') and bus_vehicle.inRepairShop:
            raise ValueError("The bus is currently in repair and cannot be assigned.")
        
        # Create new assignment
        new_assignment = RouteAssignment(date=_date, bus=bus_vehicle, route=route_obj, schedules=[])
        self.btms.assignments.append(new_assignment)
        
        # Update references
        bus_vehicle.assignments.append(new_assignment)
        route_obj.assignments.append(new_assignment)
        
        return new_assignment