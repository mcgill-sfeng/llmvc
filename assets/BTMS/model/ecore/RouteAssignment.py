from pyecore.ecore import *


class RouteAssignment(EObject, metaclass=MetaEClass):

    date = EAttribute(eType=EDate, unique=True, derived=False, changeable=True)
    bus = EReference(ordered=True, unique=True, containment=False, derived=False)
    route = EReference(ordered=True, unique=True, containment=False, derived=False)
    schedules = EReference(ordered=True, unique=True, containment=False, derived=False, upper=-1)

    def __init__(self, *, date=None, bus=None, route=None, schedules=None):
        # if kwargs:
        #    raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if date is not None:
            self.date = date

        if bus is not None:
            self.bus = bus

        if route is not None:
            self.route = route

        if schedules:
            self.schedules.extend(schedules)
