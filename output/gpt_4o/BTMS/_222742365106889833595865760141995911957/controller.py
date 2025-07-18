from datetime import date
from assets.BTMS.model.umple import *

class BTMSController:
    def __init__(self):
        self.btms = BTMS()

    def create_driver(self, drivername: str):
        # Assuming the BTMS model has a method `add_driver` to create a new driver
        try:
            self.btms.add_driver(drivername)
            print(f"Driver '{drivername}' created successfully.")
        except Exception as e:
            print(f"Failed to create driver '{drivername}': {e}")

    def create_route(self, number: int):
        # Assuming the BTMS model has a method `add_route` to create a new route
        try:
            self.btms.add_route(number)
            print(f"Route '{number}' created successfully.")
        except Exception as e:
            print(f"Failed to create route '{number}': {e}")

    def create_route_assignment(self, licensePlate: str, route: int, _date: date):
        # Assuming the BTMS model has a method `assign_route` to create a new route assignment
        try:
            self.btms.assign_route(licensePlate, route, _date)
            print(f"Route assignment for license plate '{licensePlate}' on route '{route}' for date '{_date}' created successfully.")
        except Exception as e:
            print(f"Failed to create route assignment for license plate '{licensePlate}' on route '{route}' for date '{_date}': {e}")