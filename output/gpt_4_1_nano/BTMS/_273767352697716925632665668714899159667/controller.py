from datetime import date, timedelta
from assets.BTMS.model.ecore import *

class BTMSController:
    def __init__(self):
        self.btms = BTMS()

    def create_driver(self, drivername: str):
        # Validate driver name
        if not drivername or not drivername.strip():
            raise ValueError("The name of a driver cannot be empty.")
        # Create and add driver
        driver = Driver(name=drivername, schedules=[])
        self.btms.drivers.append(driver)

    def create_route(self, number: int):
        # Validate route number
        if not isinstance(number, int):
            raise ValueError("Route number must be an integer.")
        if number <= 0:
            raise ValueError("The number of a route must be greater than zero.")
        if number > 9999:
            raise ValueError("The number of a route cannot be greater than 9999.")
        # Check for existing route with same number
        existing = next((r for r in self.btms.routes if r.number == number), None)
        if existing:
            raise ValueError("A route with this number already exists. Please use a different number.")
        # Create and add route
        route = Route(number=number, assignments=[])
        self.btms.routes.append(route)

    def create_route_assignment(self, licensePlate: str, route: int, _date: date):
        # Validate licensePlate
        if not licensePlate or not licensePlate.strip():
            raise ValueError("A bus must be specified for the assignment.")
        # Validate route
        route_obj = next((r for r in self.btms.routes if r.number == route), None)
        if route_obj is None:
            raise ValueError("A route must be specified for the assignment.")
        # Validate date: within one year from today
        today = date.today()
        delta_days = abs((_date - today).days)
        if delta_days > 365:
            raise ValueError("The date must be within a year from today.")
        # Find bus vehicle
        bus = next((b for b in self.btms.vehicles if b.licencePlate == licensePlate), None)
        if bus is None:
            # If not found, create new BusVehicle
            bus = BusVehicle(licencePlate=licensePlate, assignments=[])
            self.btms.vehicles.append(bus)
        # Create RouteAssignment
        assignment = RouteAssignment(date=_date, bus=bus, route=route_obj, schedules=[])
        # Add assignment to bus
        bus.assignments.append(assignment)
        # Add assignment to route
        route_obj.assignments.append(assignment)
        # No driver assignment here as per current feature scope