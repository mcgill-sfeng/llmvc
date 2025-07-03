from datetime import date, timedelta
from assets.BTMS.model.ecore import *

class BTMSController:
    def __init__(self):
        self.btms = BTMS()

    def create_driver(self, drivername: str):
        # Check if the driver name is valid
        if not drivername or not isinstance(drivername, str):
            raise ValueError("Driver name must be a non-empty string.")
        
        # Create a new Driver instance
        new_driver = Driver(name=drivername)
        
        # Add the new driver to the BTMS
        self.btms.drivers.append(new_driver)

    def create_route(self, number: int):
        # Check if the route number is valid
        if not (1 <= number <= 9999):
            raise ValueError("Route number must be an integer between 1 and 9999.")
        
        # Create a new Route instance
        new_route = Route(number=number)
        
        # Add the new route to the BTMS
        self.btms.routes.append(new_route)

    def create_route_assignment(self, licensePlate: str, route: int, _date: date):
        # Check if the license plate is valid
        if not licensePlate or not isinstance(licensePlate, str):
            raise ValueError("License plate must be a non-empty string.")
        
        # Check if the route number is valid
        if not (1 <= route <= 9999):
            raise ValueError("Route number must be an integer between 1 and 9999.")
        
        # Check if the date is valid (within one year from today)
        today = date.today()
        if not (today <= _date <= today + timedelta(days=365)):
            raise ValueError("Date must be within one year from today.")
        
        # Find the BusVehicle by license plate
        bus_vehicle = next((bv for bv in self.btms.vehicles if bv.licencePlate == licensePlate), None)
        if bus_vehicle is None:
            raise ValueError(f"No BusVehicle found with license plate: {licensePlate}")
        
        # Find the Route by number
        route_instance = next((r for r in self.btms.routes if r.number == route), None)
        if route_instance is None:
            raise ValueError(f"No Route found with number: {route}")
        
        # Create a new RouteAssignment instance
        new_assignment = RouteAssignment(date=_date, bus=bus_vehicle, route=route_instance)
        
        # Add the new assignment to the BTMS
        self.btms.assignments.append(new_assignment)