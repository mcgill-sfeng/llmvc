from datetime import date, timedelta
from assets.BTMS.model.ecore import *

class BTMSController:
    def __init__(self):
        self.btms = BTMS()

    def create_driver(self, drivername: str):
        # Check if a driver with the same name already exists
        for driver in self.btms.drivers:
            if driver.name == drivername:
                # Driver with this name already exists; do nothing or raise an error
                return
        # Create new Driver and add to BTMS
        new_driver = Driver(name=drivername, schedules=[])
        self.btms.drivers.append(new_driver)

    def create_route(self, number: int):
        # Validate route number
        if not (1 <= number <= 9999):
            # Invalid route number; do nothing or raise an error
            return
        # Check if route with same number exists
        for route in self.btms.routes:
            if route.number == number:
                # Route already exists; do nothing or raise an error
                return
        # Create new Route and add to BTMS
        new_route = Route(number=number, assignments=[])
        self.btms.routes.append(new_route)

    def create_route_assignment(self, licensePlate: str, route: int, _date: date):
        # Validate date: must be within one year from today
        today = date.today()
        one_year_later = today + timedelta(days=365)
        if not (today <= _date <= one_year_later):
            # Date out of range; do nothing or raise an error
            return

        # Find the BusVehicle with the given licensePlate
        bus = None
        for vehicle in self.btms.vehicles:
            if vehicle.licencePlate == licensePlate:
                bus = vehicle
                break
        if bus is None:
            # BusVehicle not found; create it
            bus = BusVehicle(licencePlate=licensePlate, assignments=[])
            self.btms.vehicles.append(bus)

        # Find the Route with the given number
        route_obj = None
        for r in self.btms.routes:
            if r.number == route:
                route_obj = r
                break
        if route_obj is None:
            # Route not found; create it
            route_obj = Route(number=route, assignments=[])
            self.btms.routes.append(route_obj)

        # Create the RouteAssignment
        new_assignment = RouteAssignment(date=_date, bus=bus, route=route_obj, schedules=[])
        self.btms.assignments.append(new_assignment)

        # Link the assignment to bus and route
        bus.assignments.append(new_assignment)
        route_obj.assignments.append(new_assignment)