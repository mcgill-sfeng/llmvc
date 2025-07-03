from datetime import date, timedelta
from assets.BTMS.model.ecore import *

class BTMSController:
    def __init__(self):
        self.btms = BTMS()

    def create_driver(self, drivername: str):
        # Create a new Driver with the given name
        driver = Driver(name=drivername)
        self.btms.drivers.add(driver)

    def create_route(self, number: int):
        # Validate route number
        if not (1 <= number <= 9999):
            raise ValueError("Route number must be between 1 and 9999.")
        # Check if route with same number already exists
        existing = next((r for r in self.btms.routes if r.number == number), None)
        if existing:
            # Optionally, do nothing or raise an error
            return
        route = Route(number=number)
        self.btms.routes.add(route)

    def create_route_assignment(self, licensePlate: str, route: int, _date: date):
        # Validate date: must be within one year from today
        today = date.today()
        one_year_later = today + timedelta(days=365)
        if not (today <= _date <= one_year_later):
            raise ValueError("Date must be within one year from today.")

        # Find the BusVehicle with the given licensePlate
        bus = next((b for b in self.btms.vehicles if b.licencePlate == licensePlate), None)
        if not bus:
            # If not found, create a new BusVehicle
            bus = BusVehicle(licencePlate=licensePlate)
            self.btms.vehicles.add(bus)

        # Find the Route with the given number
        route_obj = next((r for r in self.btms.routes if r.number == route), None)
        if not route_obj:
            # If not found, create a new Route
            route_obj = Route(number=route)
            self.btms.routes.add(route_obj)

        # Create the RouteAssignment
        assignment = RouteAssignment(date=_date, bus=bus, route=route_obj)
        self.btms.assignments.add(assignment)

        # Link the assignment to bus and route
        bus.assignments.add(assignment)
        route_obj.assignments.add(assignment)