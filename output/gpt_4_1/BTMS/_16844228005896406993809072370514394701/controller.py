from datetime import date, timedelta
from assets.BTMS.model.umple import *

class BTMSController:
    def __init__(self):
        self.btms = BTMS()

    def create_driver(self, drivername: str):
        # Validate input
        if not isinstance(drivername, str) or not drivername.strip():
            raise ValueError("Driver name must be a non-empty string.")

        # Check for uniqueness (by name)
        for i in range(self.btms.numberOfDrivers()):
            driver = self.btms.getDriver(i)
            if driver.getName() == drivername:
                raise ValueError(f"Driver with name '{drivername}' already exists.")

        # Create and add driver
        driver = Driver(drivername, self.btms)
        self.btms.addDriver2(driver)
        return driver

    def create_route(self, number: int):
        # Validate input
        if not isinstance(number, int) or not (1 <= number <= 9999):
            raise ValueError("Route number must be an integer between 1 and 9999.")

        # Check for uniqueness
        for i in range(self.btms.numberOfRoutes()):
            route = self.btms.getRoute(i)
            if route.getNumber() == number:
                raise ValueError(f"Route with number '{number}' already exists.")

        # Create and add route
        route = Route(number, self.btms)
        self.btms.addRoute2(route)
        return route

    def create_route_assignment(self, licensePlate: str, route: int, _date: date):
        # Validate licensePlate
        if not isinstance(licensePlate, str) or not licensePlate.strip():
            raise ValueError("License plate must be a non-empty string.")

        # Validate route number
        if not isinstance(route, int) or not (1 <= route <= 9999):
            raise ValueError("Route number must be an integer between 1 and 9999.")

        # Validate date
        if not isinstance(_date, date):
            raise ValueError("Date must be a datetime.date object.")
        today = date.today()
        one_year_later = today + timedelta(days=365)
        if not (today <= _date <= one_year_later):
            raise ValueError("Date must be within one year from today.")

        # Find BusVehicle by licensePlate
        bus = None
        for i in range(self.btms.numberOfVehicles()):
            v = self.btms.getVehicle(i)
            if v.getLicencePlate() == licensePlate:
                bus = v
                break
        if bus is None:
            raise ValueError(f"BusVehicle with license plate '{licensePlate}' does not exist.")

        # Find Route by number
        route_obj = None
        for i in range(self.btms.numberOfRoutes()):
            r = self.btms.getRoute(i)
            if r.getNumber() == route:
                route_obj = r
                break
        if route_obj is None:
            raise ValueError(f"Route with number '{route}' does not exist.")

        # Check for duplicate assignment (same bus, same route, same date)
        for i in range(self.btms.numberOfAssignments()):
            assignment = self.btms.getAssignment(i)
            if (assignment.getBus() == bus and
                assignment.getRoute() == route_obj and
                assignment.getDate() == _date):
                raise ValueError("This route assignment already exists.")

        # Create and add assignment
        assignment = RouteAssignment(_date, bus, route_obj, self.btms)
        self.btms.addAssignment2(assignment)
        return assignment