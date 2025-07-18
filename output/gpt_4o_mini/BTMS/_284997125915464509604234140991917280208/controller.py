from datetime import date
from assets.BTMS.model.umple import *

class BTMSController:
    def __init__(self):
        self.btms = BTMS()

    def create_driver(self, drivername: str):
        """Creates a new driver with the given name."""
        if not drivername:
            raise ValueError("Driver name cannot be empty.")
        
        # Assuming the BTMS class has a method to add a driver
        result = self.btms.add_driver(drivername)
        if result:
            return f"Driver '{drivername}' created successfully."
        else:
            raise Exception("Failed to create driver.")

    def create_route(self, number: int):
        """Creates a new route with the given route number."""
        if number <= 0:
            raise ValueError("Route number must be a positive integer.")
        
        # Assuming the BTMS class has a method to add a route
        result = self.btms.add_route(number)
        if result:
            return f"Route '{number}' created successfully."
        else:
            raise Exception("Failed to create route.")

    def create_route_assignment(self, licensePlate: str, route: int, _date: date):
        """Assigns a route to a vehicle on a specific date."""
        if not licensePlate:
            raise ValueError("License plate cannot be empty.")
        if route <= 0:
            raise ValueError("Route number must be a positive integer.")
        if not isinstance(_date, date):
            raise ValueError("Invalid date provided.")
        
        # Assuming the BTMS class has a method to assign a route to a vehicle
        result = self.btms.assign_route(licensePlate, route, _date)
        if result:
            return f"Route '{route}' assigned to vehicle '{licensePlate}' on '{_date}' successfully."
        else:
            raise Exception("Failed to assign route.")