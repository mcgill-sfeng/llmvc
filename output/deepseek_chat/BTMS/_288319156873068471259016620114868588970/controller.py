from datetime import date
from assets.BTMS.model.umple import *


class BTMSController:
    def __init__(self):
        self.btms = BTMS()

    def create_driver(self, drivername: str):
        if not drivername:
            raise ValueError("The name of a driver cannot be empty.")
        
        # Check if driver with this name already exists
        existing_drivers = [d for d in self.btms.getDrivers() if d.getName() == drivername]
        if existing_drivers:
            raise ValueError(f"A driver with name '{drivername}' already exists.")
            
        driver = self.btms.addDriver()
        driver.setName(drivername)
        return driver

    def create_route(self, number: int):
        if number <= 0:
            raise ValueError("The number of a route must be greater than zero.")
        if number > 9999:
            raise ValueError("The number of a route cannot be greater than 9999.")
            
        # Check if route with this number already exists
        existing_routes = [r for r in self.btms.getRoutes() if r.getNumber() == number]
        if existing_routes:
            raise ValueError("A route with this number already exists. Please use a different number.")
            
        route = self.btms.addRoute()
        route.setNumber(number)
        return route

    def create_route_assignment(self, licensePlate: str, route: int, _date: date):
        # Validate bus vehicle exists and is not in repair
        bus_vehicles = [v for v in self.btms.getVehicles() if v.getLicencePlate() == licensePlate]
        if not bus_vehicles:
            raise ValueError("A bus must be specified for the assignment.")
        bus = bus_vehicles[0]
        
        # Validate route exists
        routes = [r for r in self.btms.getRoutes() if r.getNumber() == route]
        if not routes:
            raise ValueError("A route must be specified for the assignment.")
        route_obj = routes[0]
        
        # Validate date is within a year from today
        today = date.today()
        if _date < today or _date > date(today.year + 1, today.month, today.day):
            raise ValueError("The date must be within a year from today.")
        
        # Check if assignment already exists for this bus on this date
        existing_assignments = [a for a in self.btms.getAssignments() 
                              if a.getBus() == bus and a.getDate() == _date]
        if existing_assignments:
            raise ValueError("This bus is already assigned to a route on this date.")
        
        # Create the assignment
        assignment = self.btms.addRouteAssignment()
        assignment.setDate(_date)
        assignment.setBus(bus)
        assignment.setRoute(route_obj)
        
        return assignment