from datetime import date
from assets.BTMS.model.ecore import *

class BTMSController:
    def __init__(self):
        self.btms = BTMS()

    def create_driver(self, drivername: str):
        # Check if driver already exists (by name)
        for driver in self.btms.drivers:
            if getattr(driver, 'name', None) == drivername:
                return driver  # Already exists, return existing

        # Create new driver
        Driver = type(self.btms.drivers[0]) if self.btms.drivers else None
        if not Driver:
            # Try to get Driver class from model_layer
            from assets.BTMS.model.ecore import Driver as DriverClass
            Driver = DriverClass

        new_driver = Driver()
        new_driver.name = drivername
        # Initialize schedules if not already
        if not hasattr(new_driver, 'schedules'):
            new_driver.schedules = []
        self.btms.drivers.append(new_driver)
        return new_driver

    def create_route(self, number: int):
        # Check if route already exists (by number)
        for route in self.btms.routes:
            if getattr(route, 'number', None) == number:
                return route  # Already exists

        # Create new route
        Route = type(self.btms.routes[0]) if self.btms.routes else None
        if not Route:
            from assets.BTMS.model.ecore import Route as RouteClass
            Route = RouteClass

        new_route = Route()
        new_route.number = number
        if not hasattr(new_route, 'assignments'):
            new_route.assignments = []
        self.btms.routes.append(new_route)
        return new_route

    def create_route_assignment(self, licensePlate: str, route: int, _date: date):
        # Find bus by licensePlate
        bus = None
        for v in self.btms.vehicles:
            if getattr(v, 'licencePlate', None) == licensePlate:
                bus = v
                break
        if not bus:
            raise ValueError(f"Bus with license plate '{licensePlate}' not found.")

        # Find route by number
        route_obj = None
        for r in self.btms.routes:
            if getattr(r, 'number', None) == route:
                route_obj = r
                break
        if not route_obj:
            raise ValueError(f"Route with number '{route}' not found.")

        # Create new RouteAssignment
        RouteAssignment = type(self.btms.assignments[0]) if self.btms.assignments else None
        if not RouteAssignment:
            from assets.BTMS.model.ecore import RouteAssignment as RouteAssignmentClass
            RouteAssignment = RouteAssignmentClass

        new_assignment = RouteAssignment()
        new_assignment.date = _date
        new_assignment.bus = bus
        new_assignment.route = route_obj
        if not hasattr(new_assignment, 'schedules'):
            new_assignment.schedules = []

        # Add assignment to bus and route
        if not hasattr(bus, 'assignments'):
            bus.assignments = []
        if not hasattr(route_obj, 'assignments'):
            route_obj.assignments = []
        bus.assignments.append(new_assignment)
        route_obj.assignments.append(new_assignment)

        self.btms.assignments.append(new_assignment)
        return new_assignment