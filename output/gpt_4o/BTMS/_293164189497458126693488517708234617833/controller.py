from datetime import date
from assets.BTMS.model.ecore import *

class BTMSController:
    def __init__(self):
        self.btms = BTMS()

    def create_driver(self, drivername: str):
        # Assuming BTMS has a method to add a driver
        try:
            self.btms.add_driver(drivername)
            print(f"Driver '{drivername}' created successfully.")
        except Exception as e:
            print(f"Failed to create driver '{drivername}': {e}")

    def create_route(self, number: int):
        # Assuming BTMS has a method to add a route
        try:
            self.btms.add_route(number)
            print(f"Route '{number}' created successfully.")
        except Exception as e:
            print(f"Failed to create route '{number}': {e}")

    def create_route_assignment(self, licensePlate: str, route: int, _date: date):
        # Assuming BTMS has a method to assign a route to a bus
        try:
            self.btms.assign_route(licensePlate, route, _date)
            print(f"Route '{route}' assigned to bus '{licensePlate}' on '{_date}' successfully.")
        except Exception as e:
            print(f"Failed to assign route '{route}' to bus '{licensePlate}' on '{_date}': {e}")