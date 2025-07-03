from datetime import date
from assets.BTMS.model.ecore import *

class BTMSController:
    def __init__(self):
        self.btms = BTMS()

    def create_driver(self, drivername: str):
        # Create a new Driver instance with the given name
        driver = Driver(name=drivername, schedules=[])
        # Add the driver to the BTMS's list of drivers
        self.btms.drivers.append(driver)

    def create_route(self, number: int):
        # Create a new Route instance with the given number
        route = Route(number=number, assignments=[])
        # Add the route to the BTMS's list of routes
        self.btms.routes.append(route)

    def create_route_assignment(self, licensePlate: str, route: int, _date: date):
        # Find the BusVehicle with the given licensePlate
        vehicle = None
        for v in self.btms.vehicles:
            if v.licencePlate == licensePlate:
                vehicle = v
                break
        if vehicle is None:
            # If not found, create a new BusVehicle and add to the list
            vehicle = BusVehicle(licencePlate=licensePlate, assignments=[])
            self.btms.vehicles.append(vehicle)

        # Find the Route with the given number
        route_obj = None
        for r in self.btms.routes:
            if r.number == route:
                route_obj = r
                break
        if route_obj is None:
            # If not found, create a new Route and add to the list
            route_obj = Route(number=route, assignments=[])
            self.btms.routes.append(route_obj)

        # Create a new RouteAssignment
        assignment = RouteAssignment(
            date=_date,
            bus=vehicle,
            route=route_obj,
            schedules=[]
        )

        # Add the assignment to the BTMS's list of assignments
        self.btms.assignments.append(assignment)

        # Link the assignment to the vehicle and route
        vehicle.assignments.append(assignment)
        route_obj.assignments.append(assignment)