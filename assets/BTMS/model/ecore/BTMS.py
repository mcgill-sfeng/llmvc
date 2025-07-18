"""Definition of meta model 'btms'."""
from pyecore.ecore import *


class BTMS(EObject, metaclass=MetaEClass):

    vehicles = EReference(ordered=True, unique=True, containment=True, derived=False, upper=-1)
    routes = EReference(ordered=True, unique=True, containment=True, derived=False, upper=-1)
    assignments = EReference(ordered=True, unique=True, containment=True, derived=False, upper=-1)
    drivers = EReference(ordered=True, unique=True, containment=True, derived=False, upper=-1)
    schedules = EReference(ordered=True, unique=True, containment=True, derived=False, upper=-1)

    def __init__(self, *, vehicles=None, routes=None, assignments=None, drivers=None, schedules=None):
        # if kwargs:
        #    raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if vehicles:
            self.vehicles.extend(vehicles)

        if routes:
            self.routes.extend(routes)

        if assignments:
            self.assignments.extend(assignments)

        if drivers:
            self.drivers.extend(drivers)

        if schedules:
            self.schedules.extend(schedules)
