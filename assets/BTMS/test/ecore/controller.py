from datetime import date

from pyecore.ecore import EDate

from assets.BTMS.model.ecore import BTMS, Driver, Route, RouteAssignment


class BTMSController:
    def __init__(self):
        self.btms = BTMS()


    def create_driver(self, drivername: str):
        if not drivername:
            raise ValueError('The name of a driver cannot be empty.')

        self.btms.drivers.append(Driver(name=drivername))


    def create_route(self, number: int):
        if number <= 0:
            raise ValueError('The number of a route must be greater than zero.')

        if number > 9999:
            raise ValueError('The number of a route cannot be greater than 9999.')

        if any(route.number == number for route in self.btms.routes):
            raise ValueError('A route with this number already exists. Please use a different number.')

        self.btms.routes.append(Route(number=number))


    def create_route_assignment(self, licensePlate: str, route: int, _date: date):
        if not any(vehicle.licencePlate == licensePlate for vehicle in self.btms.vehicles):
            raise ValueError('A bus must be specified for the assignment.')

        if not any((_route.number == route) for _route in self.btms.routes):
            raise ValueError('A route must be specified for the assignment.')

        if not _date <= date.today().replace(year=date.today().year + 1):
            raise ValueError('The date must be within a year from today.')

        vehicle = next(vehicle for vehicle in self.btms.vehicles if vehicle.licencePlate == licensePlate)
        route = next(_route for _route in self.btms.routes if _route.number == route)

        edate = EDate.from_string(_date.strftime('%Y-%m-%dT%H:%M:%S.%f%z'))
        route_assignment = RouteAssignment(date=edate, route=route, bus=vehicle)

        self.btms.assignments.append(route_assignment)
        vehicle.assignments.append(route_assignment)
