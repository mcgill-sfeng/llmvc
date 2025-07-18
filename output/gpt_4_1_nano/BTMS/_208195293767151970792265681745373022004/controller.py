from datetime import date, timedelta
from assets.BTMS.model.ecore import *

class BTMSController:
    def __init__(self):
        self.btms = BTMS()

    def create_driver(self, drivername: str):
        # Validate driver name
        if not drivername or drivername.strip() == "":
            raise ValueError("The name of a driver cannot be empty.")
        # Check if a driver with the same name already exists
        for driver in self.btms.drivers:
            if driver.name == drivername:
                # If driver exists, do not create duplicate
                return
        # Create and add new driver
        new_driver = Driver()
        new_driver.name = drivername
        self.btms.drivers.append(new_driver)

    def create_route(self, number: int):
        # Validate route number
        if not isinstance(number, int):
            raise ValueError("Route number must be an integer.")
        if number <= 0:
            raise ValueError("The number of a route must be greater than zero.")
        if number > 9999:
            raise ValueError("The number of a route cannot be greater than 9999.")
        # Check for existing route with same number
        for route in self.btms.routes:
            if route.number == number:
                raise ValueError("A route with this number already exists. Please use a different number.")
        # Create and add new route
        new_route = Route()
        new_route.number = number
        self.btms.routes.append(new_route)

    def create_route_assignment(self, licensePlate: str, route: int, _date: date):
        # Validate licensePlate
        if not licensePlate or licensePlate.strip() == "":
            raise ValueError("A bus must be specified for the assignment.")
        # Validate route number
        route_obj = None
        for r in self.btms.routes:
            if r.number == route:
                route_obj = r
                break
        if route_obj is None:
            raise ValueError("A route must be specified for the assignment.")
        # Validate bus vehicle
        bus_obj = None
        for bus in self.btms.vehicles:
            if bus.licencePlate == licensePlate:
                bus_obj = bus
                break
        if bus_obj is None:
            # If bus does not exist, create it
            bus_obj = BusVehicle()
            bus_obj.licencePlate = licensePlate
            bus_obj.assignments = []
            self.btms.vehicles.append(bus_obj)
        # Validate date: must be within one year from today
        today = date.today()
        delta_days = abs((_date - today).days)
        if delta_days > 365:
            raise ValueError("The date must be within a year from today.")
        # Check if an assignment for this bus on this date already exists
        for assignment in self.btms.assignments:
            if assignment.bus and assignment.bus.licencePlate == licensePlate and assignment.date == _date:
                # Allow multiple assignments on different routes/dates
                pass
        # Create new RouteAssignment
        new_assignment = RouteAssignment()
        new_assignment.date = _date
        new_assignment.bus = bus_obj
        new_assignment.route = route_obj
        new_assignment.schedules = []
        # Add to system
        self.btms.assignments.append(new_assignment)
        # Link assignment to bus
        if bus_obj.assignments is None:
            bus_obj.assignments = []
        bus_obj.assignments.append(new_assignment)
        # Link assignment to route
        if route_obj.assignments is None:
            route_obj.assignments = []
        route_obj.assignments.append(new_assignment)