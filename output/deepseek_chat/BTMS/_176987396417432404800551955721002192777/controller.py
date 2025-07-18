from datetime import date, timedelta
from assets.BTMS.model.ecore import *


class BTMSController:
    def __init__(self):
        self.btms = BTMS(vehicles=[], routes=[], assignments=[], drivers=[], schedules=[])

    def create_driver(self, drivername: str):
        if not drivername:
            raise ValueError("The name of a driver cannot be empty.")
        
        # Check if driver with same name already exists (assuming names must be unique)
        for driver in self.btms.drivers:
            if driver.name == drivername:
                raise ValueError("A driver with this name already exists.")
        
        new_driver = Driver(name=drivername, schedules=[])
        self.btms.drivers.append(new_driver)
        return new_driver

    def create_route(self, number: int):
        if number <= 0:
            raise ValueError("The number of a route must be greater than zero.")
        if number > 9999:
            raise ValueError("The number of a route cannot be greater than 9999.")
        
        # Check if route with this number already exists
        for route in self.btms.routes:
            if route.number == number:
                raise ValueError("A route with this number already exists. Please use a different number.")
        
        new_route = Route(number=number, assignments=[])
        self.btms.routes.append(new_route)
        return new_route

    def create_route_assignment(self, licensePlate: str, route: int, _date: date):
        # Validate date is within one year from today
        today = date(2021, 10, 7)  # As per background in scenario
        one_year_later = today + timedelta(days=365)
        
        if _date < today or _date > one_year_later:
            raise ValueError("The date must be within a year from today.")
        
        # Find the bus vehicle
        bus_vehicle = None
        for vehicle in self.btms.vehicles:
            if vehicle.licencePlate == licensePlate:
                bus_vehicle = vehicle
                break
        
        if not bus_vehicle:
            raise ValueError("A bus must be specified for the assignment.")
        
        # Check if bus is in repair shop
        if bus_vehicle.inRepairShop:
            raise ValueError("This bus is currently in the repair shop and cannot be assigned.")
        
        # Find the route
        route_obj = None
        for r in self.btms.routes:
            if r.number == route:
                route_obj = r
                break
        
        if not route_obj:
            raise ValueError("A route must be specified for the assignment.")
        
        # Check if this bus is already assigned to any route on this date
        for assignment in self.btms.assignments:
            if assignment.bus == bus_vehicle and assignment.date == _date:
                raise ValueError("This bus is already assigned to another route on this date.")
        
        # Create the new assignment
        new_assignment = RouteAssignment(date=_date, bus=bus_vehicle, route=route_obj, schedules=[])
        self.btms.assignments.append(new_assignment)
        
        # Update the bus vehicle's assignments
        bus_vehicle.assignments.append(new_assignment)
        
        # Update the route's assignments
        route_obj.assignments.append(new_assignment)
        
        return new_assignment