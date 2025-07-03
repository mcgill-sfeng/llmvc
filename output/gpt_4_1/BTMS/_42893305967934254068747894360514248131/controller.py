from datetime import date, timedelta
from assets.BTMS.model.ecore import *

class BTMSController:
    def __init__(self):
        self.btms = BTMS()

    def create_driver(self, drivername: str):
        # Validate input
        if not isinstance(drivername, str) or not drivername.strip():
            raise ValueError("Driver name must be a non-empty string.")

        # Check uniqueness
        for d in self.btms.drivers:
            if d.name == drivername:
                raise ValueError(f"Driver with name '{drivername}' already exists.")

        # Create and add driver
        driver = Driver(name=drivername)
        self.btms.drivers.append(driver)
        return driver

    def create_route(self, number: int):
        # Validate input
        if not isinstance(number, int):
            raise ValueError("Route number must be an integer.")
        if not (1 <= number <= 9999):
            raise ValueError("Route number must be between 1 and 9999.")

        # Check uniqueness
        for r in self.btms.routes:
            if r.number == number:
                raise ValueError(f"Route with number '{number}' already exists.")

        # Create and add route
        route = Route(number=number)
        self.btms.routes.append(route)
        return route

    def create_route_assignment(self, licensePlate: str, route: int, _date: date):
        # Validate licensePlate
        if not isinstance(licensePlate, str) or not licensePlate.strip():
            raise ValueError("License plate must be a non-empty string.")

        # Validate date
        if not isinstance(_date, date):
            raise ValueError("Date must be a datetime.date instance.")
        today = date.today()
        one_year_later = today + timedelta(days=365)
        if not (today <= _date <= one_year_later):
            raise ValueError("Date must be within one year from today.")

        # Find BusVehicle by licensePlate
        bus = None
        for v in self.btms.vehicles:
            if v.licencePlate == licensePlate:
                bus = v
                break
        if bus is None:
            raise ValueError(f"BusVehicle with license plate '{licensePlate}' does not exist.")

        # Find Route by number
        route_obj = None
        for r in self.btms.routes:
            if r.number == route:
                route_obj = r
                break
        if route_obj is None:
            raise ValueError(f"Route with number '{route}' does not exist.")

        # Check for duplicate assignment (same bus, route, date)
        for assignment in self.btms.assignments:
            if (assignment.bus == bus and assignment.route == route_obj and assignment.date == _date):
                raise ValueError("This bus is already assigned to this route on this date.")

        # Create and add RouteAssignment
        assignment = RouteAssignment(date=_date, bus=bus, route=route_obj)
        self.btms.assignments.append(assignment)
        # Maintain bidirectional references
        bus.assignments.append(assignment)
        route_obj.assignments.append(assignment)
        return assignment