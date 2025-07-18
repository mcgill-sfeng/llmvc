from datetime import date, timedelta
from assets.BTMS.model.ecore import *

class BTMSController:
    def __init__(self):
        self.btms = BTMS(vehicles=[], routes=[], assignments=[], drivers=[], schedules=[])

    def create_driver(self, drivername: str):
        # Check if the driver already exists
        for driver in self.btms.drivers:
            if driver.name == drivername:
                raise ValueError("Driver with this name already exists.")
        
        # Create a new Driver and add to the BTMS
        new_driver = Driver(name=drivername, schedules=[])
        self.btms.drivers.append(new_driver)

    def create_route(self, number: int):
        # Check if the route number is valid and does not already exist
        if number < 1 or number > 9999:
            raise ValueError("Route number must be between 1 and 9999.")
        
        for route in self.btms.routes:
            if route.number == number:
                raise ValueError("Route with this number already exists.")
        
        # Create a new Route and add to the BTMS
        new_route = Route(number=number, assignments=[])
        self.btms.routes.append(new_route)

    def create_route_assignment(self, licensePlate: str, route: int, _date: date):
        # Check if the date is valid (within one year from today)
        today = date.today()
        if not (today <= _date <= today + timedelta(days=365)):
            raise ValueError("Date must be within one year from today.")
        
        # Find the BusVehicle by license plate
        bus = next((vehicle for vehicle in self.btms.vehicles if vehicle.licencePlate == licensePlate), None)
        if bus is None:
            raise ValueError("Bus with this license plate does not exist.")
        
        # Find the Route by number
        route_obj = next((r for r in self.btms.routes if r.number == route), None)
        if route_obj is None:
            raise ValueError("Route with this number does not exist.")
        
        # Create a new RouteAssignment and add to the BTMS
        new_assignment = RouteAssignment(date=_date, bus=bus, route=route_obj, schedules=[])
        self.btms.assignments.append(new_assignment)
        bus.assignments.append(new_assignment)
        route_obj.assignments.append(new_assignment)