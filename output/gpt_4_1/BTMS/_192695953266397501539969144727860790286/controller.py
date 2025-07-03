from datetime import date, timedelta
from assets.BTMS.model.ecore import *

class BTMSController:
    def __init__(self):
        self.btms = BTMS(
            vehicles=[],
            routes=[],
            assignments=[],
            drivers=[],
            schedules=[]
        )

    def create_driver(self, drivername: str):
        # Validate drivername
        if not isinstance(drivername, str) or not drivername.strip():
            raise ValueError("Driver name must be a non-empty string.")

        # Check uniqueness by name
        for driver in self.btms.drivers:
            if driver.name == drivername:
                raise ValueError(f"Driver with name '{drivername}' already exists.")

        # Create and add driver
        driver = Driver(name=drivername, schedules=[])
        self.btms.drivers.append(driver)
        return driver

    def create_route(self, number: int):
        # Validate route number
        if not isinstance(number, int) or not (1 <= number <= 9999):
            raise ValueError("Route number must be an integer between 1 and 9999.")

        # Check uniqueness by number
        for route in self.btms.routes:
            if route.number == number:
                raise ValueError(f"Route with number '{number}' already exists.")

        # Create and add route
        route = Route(number=number, assignments=[])
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

        # Create RouteAssignment
        assignment = RouteAssignment(date=_date, bus=bus, route=route_obj, schedules=[])
        self.btms.assignments.append(assignment)
        bus.assignments.append(assignment)
        route_obj.assignments.append(assignment)
        return assignment