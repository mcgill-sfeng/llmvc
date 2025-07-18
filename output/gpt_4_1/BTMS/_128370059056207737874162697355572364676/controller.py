from datetime import date, timedelta
from assets.BTMS.model.ecore import *

class BTMSController:
    def __init__(self):
        self.btms = BTMS()

    def create_driver(self, drivername: str):
        # Validate drivername
        if not isinstance(drivername, str) or not drivername.strip():
            raise ValueError("Driver name must be a non-empty string.")

        # Check for duplicate driver name (assuming name must be unique)
        for driver in self.btms.getDrivers():
            if driver.getName() == drivername:
                raise ValueError(f"Driver with name '{drivername}' already exists.")

        # Create and add driver
        driver = self.btms.addDriver()
        driver.setName(drivername)
        return driver

    def create_route(self, number: int):
        # Validate route number
        if not isinstance(number, int) or not (1 <= number <= 9999):
            raise ValueError("Route number must be an integer between 1 and 9999.")

        # Check for duplicate route number
        for route in self.btms.getRoutes():
            if route.getNumber() == number:
                raise ValueError(f"Route with number {number} already exists.")

        # Create and add route
        route = self.btms.addRoute()
        route.setNumber(number)
        return route

    def create_route_assignment(self, licensePlate: str, route: int, _date: date):
        # Validate licensePlate
        if not isinstance(licensePlate, str) or not licensePlate.strip():
            raise ValueError("License plate must be a non-empty string.")

        # Validate route number
        if not isinstance(route, int) or not (1 <= route <= 9999):
            raise ValueError("Route number must be an integer between 1 and 9999.")

        # Validate _date
        if not isinstance(_date, date):
            raise ValueError("Date must be a datetime.date instance.")
        today = date.today()
        one_year_later = today + timedelta(days=365)
        if not (today <= _date <= one_year_later):
            raise ValueError("Date must be within one year from today.")

        # Find BusVehicle by licensePlate
        bus = None
        for v in self.btms.getVehicles():
            if v.getLicencePlate() == licensePlate:
                bus = v
                break
        if bus is None:
            raise ValueError(f"BusVehicle with license plate '{licensePlate}' not found.")

        # Find Route by number
        route_obj = None
        for r in self.btms.getRoutes():
            if r.getNumber() == route:
                route_obj = r
                break
        if route_obj is None:
            raise ValueError(f"Route with number {route} not found.")

        # Check for duplicate assignment for same bus, route, and date
        for assignment in self.btms.getAssignments():
            if (assignment.getBus() == bus and
                assignment.getRoute() == route_obj and
                assignment.getDate() == _date):
                raise ValueError("This bus is already assigned to this route on this date.")

        # Create and add RouteAssignment
        assignment = self.btms.addAssignment()
        assignment.setBus(bus)
        assignment.setRoute(route_obj)
        assignment.setDate(_date)
        return assignment