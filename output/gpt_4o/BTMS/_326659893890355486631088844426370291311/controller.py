from datetime import date
from assets.BTMS.model.umple import *

class BTMSController:
    def __init__(self):
        self.btms = BTMS()

    def create_driver(self, drivername: str):
        # Assuming BTMS has a method to add a driver
        # The method might be named `add_driver` and could require a unique ID
        # Since we don't have the ID generation logic, we'll assume the model handles it
        try:
            self.btms.add_driver(drivername)
            print(f"Driver '{drivername}' created successfully.")
        except Exception as e:
            print(f"Failed to create driver '{drivername}': {e}")

    def create_route(self, number: int):
        # Assuming BTMS has a method to add a route
        # The method might be named `add_route`
        if 1 <= number <= 9999:
            try:
                self.btms.add_route(number)
                print(f"Route '{number}' created successfully.")
            except Exception as e:
                print(f"Failed to create route '{number}': {e}")
        else:
            print(f"Route number '{number}' is out of valid range (1-9999).")

    def create_route_assignment(self, licensePlate: str, route: int, _date: date):
        # Assuming BTMS has a method to add a route assignment
        # The method might be named `add_route_assignment`
        # We need to ensure the date is within one year from today
        today = date.today()
        one_year_from_today = today.replace(year=today.year + 1)
        
        if today <= _date < one_year_from_today:
            try:
                self.btms.add_route_assignment(licensePlate, route, _date)
                print(f"Route assignment for bus '{licensePlate}' on route '{route}' for date '{_date}' created successfully.")
            except Exception as e:
                print(f"Failed to create route assignment for bus '{licensePlate}' on route '{route}' for date '{_date}': {e}")
        else:
            print(f"Date '{_date}' is not within the valid range (today to one year from today).")