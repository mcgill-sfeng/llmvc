from datetime import date
from assets.BTMS.model.ecore import *

class BTMSController:
    def __init__(self):
        self.btms = BTMS()

    def create_driver(self, drivername: str):
        # Check if a driver with the same name already exists
        for driver in self.btms.drivers:
            if driver.name == drivername:
                raise ValueError(f"Driver with name {drivername} already exists.")
        
        # Create a new driver
        new_driver = Driver(name=drivername)
        self.btms.drivers.append(new_driver)

    def create_route(self, number: int):
        # Validate the route number
        if not (1 <= number <= 9999):
            raise ValueError("Route number must be between 1 and 9999.")
        
        # Check if a route with the same number already exists
        for route in self.btms.routes:
            if route.number == number:
                raise ValueError(f"Route with number {number} already exists.")
        
        # Create a new route
        new_route = Route(number=number)
        self.btms.routes.append(new_route)

    def create_route_assignment(self, licensePlate: str, route: int, _date: date):
        # Validate the date
        if not (date.today() <= _date <= date.today().replace(year=date.today().year + 1)):
            raise ValueError("Date must be within one year from today.")
        
        # Find the bus vehicle by license plate
        bus_vehicle = None
        for vehicle in self.btms.vehicles:
            if vehicle.licencePlate == licensePlate:
                bus_vehicle = vehicle
                break
        if bus_vehicle is None:
            raise ValueError(f"No bus vehicle found with license plate {licensePlate}.")
        
        # Find the route by number
        route_obj = None
        for r in self.btms.routes:
            if r.number == route:
                route_obj = r
                break
        if route_obj is None:
            raise ValueError(f"No route found with number {route}.")
        
        # Create a new route assignment
        new_assignment = RouteAssignment(date=_date, bus=bus_vehicle, route=route_obj)
        self.btms.assignments.append(new_assignment)
        bus_vehicle.assignments.append(new_assignment)
        route_obj.assignments.append(new_assignment)