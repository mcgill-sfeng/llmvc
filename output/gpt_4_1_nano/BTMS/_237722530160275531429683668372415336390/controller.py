from datetime import date, timedelta
from assets.BTMS.model.ecore import *

class BTMSController:
    def __init__(self):
        self.btms = BTMS()

    def create_driver(self, drivername: str):
        # Create a new Driver with the given name
        new_driver = Driver(name=drivername, schedules=[])
        self.btms.drivers.append(new_driver)

    def create_route(self, number: int):
        # Validate route number
        if not (1 <= number <= 9999):
            raise ValueError("Route number must be between 1 and 9999.")
        # Check if route already exists
        existing_route = next((r for r in self.btms.routes if r.number == number), None)
        if existing_route:
            # Optionally, could raise an error or ignore
            return
        # Create new Route
        new_route = Route(number=number, assignments=[])
        self.btms.routes.append(new_route)

    def create_route_assignment(self, licensePlate: str, route: int, _date: date):
        # Validate date: must be within one year from today
        today = date.today()
        one_year_later = today + timedelta(days=365)
        if not (today <= _date <= one_year_later):
            raise ValueError("Date must be within one year from today.")

        # Find the BusVehicle by licensePlate
        bus = next((b for b in self.btms.vehicles if b.licencePlate == licensePlate), None)
        if bus is None:
            # If not found, create a new BusVehicle
            bus = BusVehicle(licencePlate=licensePlate, assignments=[])
            self.btms.vehicles.append(bus)

        # Find the Route by number
        route_obj = next((r for r in self.btms.routes if r.number == route), None)
        if route_obj is None:
            # If route does not exist, create it
            route_obj = Route(number=route, assignments=[])
            self.btms.routes.append(route_obj)

        # Create RouteAssignment
        assignment = RouteAssignment(date=_date, bus=bus, route=route_obj, schedules=[])
        # Append assignment to bus and route
        bus.assignments.append(assignment)
        route_obj.assignments.append(assignment)
        # Append to system's assignments list
        self.btms.assignments.append(assignment)