from datetime import date, timedelta
from assets.BTMS.model.ecore import *

class BTMSController:
    def __init__(self):
        self.btms = BTMS()

    def create_driver(self, drivername: str):
        # Check if the driver already exists
        if any(driver.name == drivername for driver in self.btms.drivers):
            raise ValueError(f"Driver with name '{drivername}' already exists.")
        
        # Create a new Driver and add it to the BTMS
        new_driver = Driver(name=drivername)
        self.btms.drivers.append(new_driver)

    def create_route(self, number: int):
        # Check if the route already exists
        if any(route.number == number for route in self.btms.routes):
            raise ValueError(f"Route with number '{number}' already exists.")
        
        # Create a new Route and add it to the BTMS
        new_route = Route(number=number)
        self.btms.routes.append(new_route)

    def create_route_assignment(self, licensePlate: str, route: int, _date: date):
        # Validate the date
        if _date < date.today() or _date > date.today() + timedelta(days=365):
            raise ValueError("Date must be within one year from today.")

        # Find the BusVehicle by license plate
        bus = next((vehicle for vehicle in self.btms.vehicles if vehicle.licencePlate == licensePlate), None)
        if bus is None:
            raise ValueError(f"Bus with license plate '{licensePlate}' does not exist.")

        # Find the Route by number
        route_obj = next((r for r in self.btms.routes if r.number == route), None)
        if route_obj is None:
            raise ValueError(f"Route with number '{route}' does not exist.")

        # Create a new RouteAssignment and add it to the BTMS
        new_assignment = RouteAssignment(date=_date, bus=bus, route=route_obj)
        self.btms.assignments.append(new_assignment)