from datetime import date, timedelta
from assets.BTMS.model.umple import *

class BTMSController:
    def __init__(self):
        self.btms = BTMS()

    def create_driver(self, drivername: str):
        # Check if a driver with the same name already exists
        for driver in self.btms.getDrivers():
            if driver.getName() == drivername:
                raise ValueError(f"Driver with name {drivername} already exists.")
        
        # Add the new driver
        self.btms.addDriver1(drivername)

    def create_route(self, number: int):
        # Validate the route number
        if not (1 <= number <= 9999):
            raise ValueError("Route number must be between 1 and 9999.")
        
        # Check if a route with the same number already exists
        for route in self.btms.getRoutes():
            if route.getNumber() == number:
                raise ValueError(f"Route with number {number} already exists.")
        
        # Add the new route
        self.btms.addRoute1(number)

    def create_route_assignment(self, licensePlate: str, route: int, _date: date):
        # Validate the date
        today = date.today()
        if not (today <= _date <= today + timedelta(days=365)):
            raise ValueError("Date must be within one year from today.")
        
        # Find the bus vehicle by license plate
        bus = None
        for vehicle in self.btms.getVehicles():
            if vehicle.getLicencePlate() == licensePlate:
                bus = vehicle
                break
        if bus is None:
            raise ValueError(f"No bus with license plate {licensePlate} found.")
        
        # Find the route by number
        route_obj = None
        for r in self.btms.getRoutes():
            if r.getNumber() == route:
                route_obj = r
                break
        if route_obj is None:
            raise ValueError(f"No route with number {route} found.")
        
        # Create the route assignment
        self.btms.addAssignment1(_date, bus, route_obj)