from datetime import date
from model_layer import BTMS


class BTMSController:
    def __init__(self):
        self.btms = BTMS()

    def create_driver(self, drivername: str):
        # TODO: implement the create_driver method
        pass

    def create_route(self, number: int):
        # TODO: implement the create_route method
        pass

    def create_route_assignment(self, licensePlate: str, route: int, _date: date):
        # TODO: implement the create_route_assignment method
        pass