from datetime import date
from assets.BTMS.model.ecore import *

class BTMSController:
    def __init__(self):
        self.btms = BTMS()

    def create_driver(self, drivername: str):
        # Create a new Driver instance with the given name
        driver = Driver(name=drivername, schedules=[])
        # Add the driver to the BTMS's drivers collection
        self.btms.drivers.append(driver)

    def create_route(self, number: int):
        # Create a new Route instance with the given number
        route = Route(number=number, assignments=[])
        # Add the route to the BTMS's routes collection
        self.btms.routes.append(route)

    def create_route_assignment(self, licensePlate: str, route: int, _date: date):
        # Find the bus vehicle with the given license plate
        bus = None
        for vehicle in self.btms.vehicles:
            if vehicle.licencePlate == licensePlate:
                bus = vehicle
                break
        if bus is None:
            # If not found, create a new BusVehicle and add it to the collection
            bus = BusVehicle(licencePlate=licensePlate, assignments=[])
            self.btms.vehicles.append(bus)

        # Find the route with the given number
        route_obj = None
        for r in self.btms.routes:
            if r.number == route:
                route_obj = r
                break
        if route_obj is None:
            # If route not found, create it
            route_obj = Route(number=route, assignments=[])
            self.btms.routes.append(route_obj)

        # Create a new RouteAssignment
        assignment = RouteAssignment(date=_date, bus=bus, route=route_obj, schedules=[])

        # Add the assignment to the bus's assignments
        bus.assignments.append(assignment)

        # Add the assignment to the route's assignments
        route_obj.assignments.append(assignment)