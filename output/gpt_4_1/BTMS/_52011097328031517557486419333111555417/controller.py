from datetime import date
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
        # Check for duplicate driver name
        for driver in self.btms.drivers:
            if driver.name == drivername:
                return driver  # Already exists, return existing

        # Create new driver
        new_driver = Driver(name=drivername, schedules=[])
        self.btms.drivers.append(new_driver)
        return new_driver

    def create_route(self, number: int):
        # Check for duplicate route number
        for route in self.btms.routes:
            if route.number == number:
                return route  # Already exists, return existing

        # Create new route
        new_route = Route(number=number, assignments=[])
        self.btms.routes.append(new_route)
        return new_route

    def create_route_assignment(self, licensePlate: str, route: int, _date: date):
        # Find or create the bus vehicle
        bus = None
        for v in self.btms.vehicles:
            if v.licencePlate == licensePlate:
                bus = v
                break
        if bus is None:
            bus = BusVehicle(licencePlate=licensePlate, assignments=[])
            self.btms.vehicles.append(bus)

        # Find or create the route
        route_obj = None
        for r in self.btms.routes:
            if r.number == route:
                route_obj = r
                break
        if route_obj is None:
            route_obj = Route(number=route, assignments=[])
            self.btms.routes.append(route_obj)

        # Check for duplicate assignment (same bus, route, and date)
        for assignment in self.btms.assignments:
            if (assignment.bus == bus and
                assignment.route == route_obj and
                assignment.date == _date):
                return assignment  # Already exists

        # Create new assignment
        new_assignment = RouteAssignment(
            date=_date,
            bus=bus,
            route=route_obj,
            schedules=[]
        )
        self.btms.assignments.append(new_assignment)
        bus.assignments.append(new_assignment)
        route_obj.assignments.append(new_assignment)
        return new_assignment