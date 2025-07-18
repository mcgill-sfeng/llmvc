from datetime import date, timedelta
from assets.BTMS.model.ecore import *
from assets.BTMS.model.ecore import *

class BTMSController:
    def __init__(self):
        self.btms = BTMS()

    def create_driver(self, drivername: str):
        # Create a new Driver with the given name
        driver = Driver(name=drivername)
        self.btms.drivers.append(driver)

    def create_route(self, number: int):
        # Create a new Route with the given number
        route = Route(number=number)
        self.btms.routes.append(route)

    def create_route_assignment(self, licensePlate: str, route: int, _date: date):
        # Validate date: must be within one year from today
        today = date.today()
        one_year_later = today + timedelta(days=365)
        if not (today <= _date <= one_year_later):
            raise ValueError("Date must be within one year from today.")

        # Find the BusVehicle with the given licensePlate
        bus = None
        for v in self.btms.vehicles:
            if v.licencePlate == licensePlate:
                bus = v
                break
        if bus is None:
            # If not found, create and add it
            bus = BusVehicle(licencePlate=licensePlate)
            self.btms.vehicles.append(bus)

        # Find the Route with the given number
        route_obj = None
        for r in self.btms.routes:
            if r.number == route:
                route_obj = r
                break
        if route_obj is None:
            # If not found, create and add it
            route_obj = Route(number=route)
            self.btms.routes.append(route_obj)

        # Create RouteAssignment
        assignment = RouteAssignment(date=_date, bus=bus, route=route_obj)

        # Add assignment to BTMS
        self.btms.assignments.append(assignment)

        # Link assignment to bus and route
        bus.assignments.append(assignment)
        route_obj.assignments.append(assignment)