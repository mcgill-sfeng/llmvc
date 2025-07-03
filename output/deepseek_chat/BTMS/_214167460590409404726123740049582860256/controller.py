from datetime import date
from assets.BTMS.model.ecore import *


class BTMSController:
    def __init__(self):
        self.btms = BTMS()

    def create_driver(self, drivername: str):
        """Creates a new driver with the given name and adds it to the system"""
        if not drivername:
            raise ValueError("Driver name cannot be empty")
        
        new_driver = Driver(name=drivername, schedules=[])
        self.btms.drivers.append(new_driver)
        return new_driver

    def create_route(self, number: int):
        """Creates a new route with the given number and adds it to the system"""
        if number <= 0:
            raise ValueError("Route number must be positive")
        
        # Check if route already exists
        if any(route.number == number for route in self.btms.routes):
            raise ValueError(f"Route {number} already exists")
            
        new_route = Route(number=number, assignments=[])
        self.btms.routes.append(new_route)
        return new_route

    def create_route_assignment(self, licensePlate: str, route: int, _date: date):
        """Creates a new route assignment for a vehicle on a specific route and date"""
        if not licensePlate:
            raise ValueError("License plate cannot be empty")
            
        if route <= 0:
            raise ValueError("Route number must be positive")
            
        if not _date or _date < date.today():
            raise ValueError("Date must be today or in the future")
            
        # Find the vehicle
        vehicle = next((v for v in self.btms.vehicles if v.licencePlate == licensePlate), None)
        if not vehicle:
            raise ValueError(f"Vehicle with license plate {licensePlate} not found")
            
        # Find the route
        route_obj = next((r for r in self.btms.routes if r.number == route), None)
        if not route_obj:
            raise ValueError(f"Route {route} not found")
            
        # Check for existing assignment on the same date
        existing_assignment = next(
            (a for a in self.btms.assignments 
             if a.date == _date and a.bus.licencePlate == licensePlate),
            None
        )
        if existing_assignment:
            raise ValueError(f"Vehicle {licensePlate} already has an assignment on {_date}")
            
        # Create new assignment
        new_assignment = RouteAssignment(
            date=_date,
            bus=vehicle,
            route=route_obj,
            schedules=[]
        )
        
        # Add to collections
        self.btms.assignments.append(new_assignment)
        vehicle.assignments.append(new_assignment)
        route_obj.assignments.append(new_assignment)
        
        return new_assignment