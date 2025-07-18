from datetime import date, timedelta
from assets.BTMS.model.umple import *

class BTMSController:
    def __init__(self):
        self.btms = BTMS()

    def create_driver(self, drivername: str):
        if not isinstance(drivername, str) or not drivername.strip():
            raise ValueError("Driver name must be a non-empty string.")

        # Check for uniqueness of driver name (assuming driver name must be unique)
        for driver in self.btms.getDrivers():
            if driver.getName() == drivername:
                raise ValueError(f"Driver with name '{drivername}' already exists.")

        # Create driver (assuming BTMS has addDriver(name) or similar)
        driver = self.btms.addDriver(drivername)
        return driver

    def create_route(self, number: int):
        if not isinstance(number, int) or not (1 <= number <= 9999):
            raise ValueError("Route number must be an integer between 1 and 9999.")

        # Check for uniqueness of route number
        for route in self.btms.getRoutes():
            if route.getNumber() == number:
                raise ValueError(f"Route with number {number} already exists.")

        # Create route (assuming BTMS has addRoute(number) or similar)
        route = self.btms.addRoute(number)
        return route

    def create_route_assignment(self, licensePlate: str, route: int, _date: date):
        if not isinstance(licensePlate, str) or not licensePlate.strip():
            raise ValueError("License plate must be a non-empty string.")

        # Find the bus vehicle by license plate
        bus = None
        for b in self.btms.getBusVehicles():
            if b.getLicensePlate() == licensePlate:
                bus = b
                break
        if bus is None:
            raise ValueError(f"Bus vehicle with license plate '{licensePlate}' does not exist.")

        # Find the route by number
        route_obj = None
        for r in self.btms.getRoutes():
            if r.getNumber() == route:
                route_obj = r
                break
        if route_obj is None:
            raise ValueError(f"Route with number {route} does not exist.")

        # Validate date
        if not isinstance(_date, date):
            raise ValueError("Date must be a datetime.date object.")
        today = date.today()
        one_year_later = today + timedelta(days=365)
        if not (today <= _date <= one_year_later):
            raise ValueError("Date must be within one year from today.")

        # Check if assignment already exists for this bus, route, and date
        for assignment in self.btms.getRouteAssignments():
            if (assignment.getBus() == bus and
                assignment.getRoute() == route_obj and
                assignment.getDate() == _date):
                raise ValueError("This route assignment already exists.")

        # Create route assignment (assuming BTMS has addRouteAssignment(bus, route, date))
        assignment = self.btms.addRouteAssignment(bus, route_obj, _date)
        return assignment