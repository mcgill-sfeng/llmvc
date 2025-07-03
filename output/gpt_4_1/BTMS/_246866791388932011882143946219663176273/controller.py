from datetime import date, timedelta
from assets.BTMS.model.ecore import *

class BTMSController:
    def __init__(self):
        self.btms = BTMS()

    def create_driver(self, drivername: str):
        if not drivername or not isinstance(drivername, str):
            raise ValueError("Driver name must be a non-empty string.")
        # Check for uniqueness: name + id (but only name is provided here)
        # We'll assume name must be unique for this controller
        for d in self.btms.drivers:
            if d.name == drivername:
                raise ValueError(f"Driver with name '{drivername}' already exists.")
        new_driver = Driver(name=drivername, schedules=[])
        self.btms.drivers.append(new_driver)
        return new_driver

    def create_route(self, number: int):
        if not isinstance(number, int) or not (1 <= number <= 9999):
            raise ValueError("Route number must be an integer between 1 and 9999.")
        for r in self.btms.routes:
            if r.number == number:
                raise ValueError(f"Route with number {number} already exists.")
        new_route = Route(number=number, assignments=[])
        self.btms.routes.append(new_route)
        return new_route

    def create_route_assignment(self, licensePlate: str, route: int, _date: date):
        # Validate licensePlate
        if not licensePlate or not isinstance(licensePlate, str):
            raise ValueError("License plate must be a non-empty string.")
        # Find BusVehicle
        bus = None
        for v in self.btms.vehicles:
            if v.licencePlate == licensePlate:
                bus = v
                break
        if bus is None:
            raise ValueError(f"BusVehicle with license plate '{licensePlate}' not found.")

        # Validate route number and find Route
        if not isinstance(route, int) or not (1 <= route <= 9999):
            raise ValueError("Route number must be an integer between 1 and 9999.")
        route_obj = None
        for r in self.btms.routes:
            if r.number == route:
                route_obj = r
                break
        if route_obj is None:
            raise ValueError(f"Route with number {route} not found.")

        # Validate date: must be within one year from today
        today = date.today()
        if not isinstance(_date, date):
            raise ValueError("Date must be a datetime.date instance.")
        if _date < today or _date > today + timedelta(days=365):
            raise ValueError("Date must be within one year from today.")

        # Create RouteAssignment
        new_assignment = RouteAssignment(date=_date, bus=bus, route=route_obj, schedules=[])
        self.btms.assignments.append(new_assignment)
        bus.assignments.append(new_assignment)
        route_obj.assignments.append(new_assignment)
        return new_assignment