from datetime import date, timedelta
from assets.BTMS.model.ecore import *
from assets.BTMS.model.ecore import *


class BTMSController:
    def __init__(self):
        self.btms = BTMS()

    def create_driver(self, drivername: str):
        if not drivername:
            raise ValueError("The name of a driver cannot be empty.")
        
        # Check if driver with same name already exists
        for driver in self.btms.drivers:
            if driver.name == drivername:
                raise ValueError("A driver with this name already exists.")
        
        new_driver = Driver(name=drivername)
        self.btms.drivers.append(new_driver)
        return new_driver

    def create_route(self, number: int):
        if number <= 0:
            raise ValueError("The number of a route must be greater than zero.")
        if number > 9999:
            raise ValueError("The number of a route cannot be greater than 9999.")
        
        # Check if route with same number already exists
        for route in self.btms.routes:
            if route.number == number:
                raise ValueError("A route with this number already exists. Please use a different number.")
        
        new_route = Route(number=number)
        self.btms.routes.append(new_route)
        return new_route

    def create_route_assignment(self, licensePlate: str, route: int, _date: date):
        # Validate inputs
        if not licensePlate:
            raise ValueError("A bus must be specified for the assignment.")
        
        # Find the bus vehicle
        bus_vehicle = None
        for vehicle in self.btms.vehicles:
            if vehicle.licencePlate == licensePlate:
                bus_vehicle = vehicle
                break
        
        if not bus_vehicle:
            raise ValueError(f"No bus found with license plate {licensePlate}.")
        
        # Find the route
        route_obj = None
        for r in self.btms.routes:
            if r.number == route:
                route_obj = r
                break
        
        if not route_obj:
            raise ValueError(f"No route found with number {route}.")
        
        # Validate date
        today = date.today()
        one_year_later = today + timedelta(days=365)
        
        if _date < today or _date > one_year_later:
            raise ValueError("The date must be within a year from today.")
        
        # Check if assignment already exists for this bus on this date
        for assignment in self.btms.assignments:
            if assignment.bus == bus_vehicle and assignment.date == _date:
                raise ValueError(f"This bus is already assigned to another route on {_date}.")
        
        # Create new assignment
        new_assignment = RouteAssignment(date=_date, bus=bus_vehicle, route=route_obj)
        self.btms.assignments.append(new_assignment)
        
        # Update references
        bus_vehicle.assignments.append(new_assignment)
        route_obj.assignments.append(new_assignment)
        
        return new_assignment