from datetime import date
from assets.BTMS.model.ecore import *
from assets.BTMS.model.ecore import *
from datetime import timedelta


class BTMSController:
    def __init__(self):
        self.btms = BTMS()

    def create_driver(self, drivername: str):
        if not drivername:
            raise ValueError("The name of a driver cannot be empty.")
        
        # Check if driver with same name already exists
        if any(d.name == drivername for d in self.btms.drivers):
            raise ValueError("A driver with this name already exists.")
            
        driver = Driver(name=drivername)
        self.btms.drivers.append(driver)
        return driver

    def create_route(self, number: int):
        if number <= 0:
            raise ValueError("The number of a route must be greater than zero.")
        if number > 9999:
            raise ValueError("The number of a route cannot be greater than 9999.")
            
        # Check if route with same number already exists
        if any(r.number == number for r in self.btms.routes):
            raise ValueError("A route with this number already exists. Please use a different number.")
            
        route = Route(number=number)
        self.btms.routes.append(route)
        return route

    def create_route_assignment(self, licensePlate: str, route: int, _date: date):
        # Validate inputs
        if not licensePlate:
            raise ValueError("A bus must be specified for the assignment.")
        if not route:
            raise ValueError("A route must be specified for the assignment.")
            
        # Check date is within one year from today
        today = date.today()
        one_year_later = today + timedelta(days=365)
        if _date < today or _date > one_year_later:
            raise ValueError("The date must be within a year from today.")
            
        # Find the bus vehicle
        bus = next((v for v in self.btms.vehicles if v.licencePlate == licensePlate), None)
        if not bus:
            raise ValueError(f"No bus found with license plate {licensePlate}")
            
        # Find the route
        route_obj = next((r for r in self.btms.routes if r.number == route), None)
        if not route_obj:
            raise ValueError(f"No route found with number {route}")
            
        # Check if bus is in repair shop
        if hasattr(bus, 'inRepairShop') and bus.inRepairShop:
            raise ValueError("Cannot assign a bus that's in the repair shop")
            
        # Create the assignment
        assignment = RouteAssignment(date=_date, bus=bus, route=route_obj)
        self.btms.assignments.append(assignment)
        
        # Link the assignment to the bus and route
        bus.assignments.append(assignment)
        route_obj.assignments.append(assignment)
        
        return assignment