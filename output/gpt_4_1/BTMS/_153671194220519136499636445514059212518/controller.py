from datetime import date
from assets.BTMS.model.ecore import *


class BTMSController:
    def __init__(self):
        self.btms = BTMS()

    def create_driver(self, drivername: str):
        """
        Creates a new driver with the given name and adds it to the BTMS model.
        Returns the created driver object.
        """
        # Assume BTMS has a method createDriver(drivername) or a drivers collection with add()
        if hasattr(self.btms, 'createDriver'):
            driver = self.btms.createDriver(drivername)
        elif hasattr(self.btms, 'drivers') and hasattr(self.btms.drivers, 'add'):
            # Fallback: create Driver instance and add to collection
            # Try to find Driver class in model_layer
            from assets.BTMS.model.ecore import Driver
            driver = Driver(drivername)
            self.btms.drivers.add(driver)
        else:
            raise NotImplementedError("BTMS model does not support driver creation.")
        return driver

    def create_route(self, number: int):
        """
        Creates a new route with the given number and adds it to the BTMS model.
        Returns the created route object.
        """
        # Assume BTMS has a method createRoute(number) or a routes collection with add()
        if hasattr(self.btms, 'createRoute'):
            route = self.btms.createRoute(number)
        elif hasattr(self.btms, 'routes') and hasattr(self.btms.routes, 'add'):
            from assets.BTMS.model.ecore import Route
            route = Route(number)
            self.btms.routes.add(route)
        else:
            raise NotImplementedError("BTMS model does not support route creation.")
        return route

    def create_route_assignment(self, licensePlate: str, route: int, _date: date):
        """
        Creates a new route assignment for the given bus (by licensePlate), route (by number), and date.
        Returns the created route assignment object.
        """
        # Find the bus by licensePlate
        bus = None
        if hasattr(self.btms, 'buses'):
            for b in self.btms.buses:
                if getattr(b, 'licensePlate', None) == licensePlate:
                    bus = b
                    break
        if bus is None:
            raise ValueError(f"Bus with license plate '{licensePlate}' not found.")

        # Find the route by number
        route_obj = None
        if hasattr(self.btms, 'routes'):
            for r in self.btms.routes:
                if getattr(r, 'number', None) == route:
                    route_obj = r
                    break
        if route_obj is None:
            raise ValueError(f"Route with number '{route}' not found.")

        # Create the route assignment
        if hasattr(self.btms, 'createRouteAssignment'):
            assignment = self.btms.createRouteAssignment(bus, route_obj, _date)
        elif hasattr(self.btms, 'routeAssignments') and hasattr(self.btms.routeAssignments, 'add'):
            from assets.BTMS.model.ecore import RouteAssignment
            assignment = RouteAssignment(bus, route_obj, _date)
            self.btms.routeAssignments.add(assignment)
        else:
            raise NotImplementedError("BTMS model does not support route assignment creation.")
        return assignment