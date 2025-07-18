from datetime import date
from assets.BTMS.model.umple import BTMS, Driver, Route, RouteAssignment


class BTMSController:
    def __init__(self):
        self.btms = BTMS()


    def create_driver(self, drivername: str):
        if not drivername:
            raise ValueError('The name of a driver cannot be empty.')

        self.btms.addDriver(drivername)


    def create_route(self, number: int):
        if number <= 0:
            raise ValueError('The number of a route must be greater than zero.')

        if number > 9999:
            raise ValueError('The number of a route cannot be greater than 9999.')

        if any(route.getNumber() == number for route in self.btms.getRoutes()):
            raise ValueError('A route with this number already exists. Please use a different number.')

        self.btms.addRoute(number)


    def create_route_assignment(self, licensePlate: str, route: int, _date: date):
        if not any(vehicle.getLicencePlate() == licensePlate for vehicle in self.btms.getVehicles()):
            raise ValueError('A bus must be specified for the assignment.')

        if not any((_route.getNumber() == route) for _route in self.btms.getRoutes()):
            raise ValueError('A route must be specified for the assignment.')

        if not _date <= date.today().replace(year=date.today().year + 1):
            raise ValueError('The date must be within a year from today.')

        vehicle = next(vehicle for vehicle in self.btms.getVehicles() if vehicle.getLicencePlate() == licensePlate)
        route = next(_route for _route in self.btms.getRoutes() if _route.getNumber() == route)

        self.btms.addAssignment(_date, vehicle, route)
