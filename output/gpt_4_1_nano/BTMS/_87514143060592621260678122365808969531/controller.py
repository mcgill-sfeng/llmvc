from datetime import date
from assets.BTMS.model.ecore import *
from assets.BTMS.model.ecore import *

class BTMSController:
    def __init__(self):
        self.btms = BTMS()

    def create_driver(self, drivername: str):
        # Create a new Driver instance with the given name
        driver = Driver(name=drivername)
        # Add the driver to the BTMS's drivers collection
        self.btms.drivers.append(driver)

    def create_route(self, number: int):
        # Create a new Route instance with the given number
        route = Route(number=number)
        # Add the route to the BTMS's routes collection
        self.btms.routes.append(route)

    def create_route_assignment(self, licensePlate: str, route: int, _date: date):
        # Find the BusVehicle with the given licensePlate
        bus = None
        for vehicle in self.btms.vehicles:
            if vehicle.licencePlate == licensePlate:
                bus = vehicle
                break
        if bus is None:
            # If not found, create a new BusVehicle and add it
            bus = BusVehicle(licencePlate=licensePlate)
            self.btms.vehicles.append(bus)

        # Find the Route with the given number
        route_obj = None
        for r in self.btms.routes:
            if r.number == route:
                route_obj = r
                break
        if route_obj is None:
            # If not found, create a new Route and add it
            route_obj = Route(number=route)
            self.btms.routes.append(route_obj)

        # Create a new RouteAssignment with the specified date, bus, and route
        assignment = RouteAssignment(date=_date, bus=bus, route=route_obj)

        # Add the assignment to the BTMS's assignments collection
        self.btms.assignments.append(assignment)

        # Link the assignment to the bus and route
        bus.assignments.append(assignment)
        route_obj.assignments.append(assignment)
        
        # Optionally, create schedules or assign drivers as needed (not specified here)
        # But for completeness, no additional steps are required unless specified