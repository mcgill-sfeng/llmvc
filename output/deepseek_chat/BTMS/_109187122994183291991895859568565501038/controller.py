from datetime import date, timedelta
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
            raise ValueError("A driver with this name already exists.")
            
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
        bus_vehicle = bus_vehicles[0]
        
        # Validate route exists
        routes = [r for r in self.btms.getRoutes() if r.getNumber() == route]
        if not routes:
            raise ValueError("A route must be specified for the assignment.")
        route_obj = routes[0]
        
        # Validate date is within one year from today
        today = date.today()
        one_year_later = today + timedelta(days=365)
        if _date < today or _date > one_year_later:
            raise ValueError("The date must be within a year from today.")
        
        # Check if this bus is already assigned to any route on this date
        existing_assignments = [a for a in self.btms.getAssignments() 
                               if a.getBus() == bus_vehicle and a.getDate() == _date]
        if existing_assignments:
            raise ValueError("This bus is already assigned to a route on this date.")
        
        # Create the assignment
        assignment = self.btms.addRouteAssignment()
        assignment.setBus(bus_vehicle)
        assignment.setRoute(route_obj)
        assignment.setDate(_date)
        
        return assignment