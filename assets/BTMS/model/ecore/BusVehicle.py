from pyecore.ecore import *

class BusVehicle(EObject, metaclass=MetaEClass):

    licencePlate = EAttribute(eType=EString, unique=True, derived=False, changeable=True)
    assignments = EReference(ordered=True, unique=True, containment=False, derived=False, upper=-1)

    def __init__(self, *, licencePlate=None, assignments=None):
        # if kwargs:
        #    raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if licencePlate is not None:
            self.licencePlate = licencePlate

        if assignments:
            self.assignments.extend(assignments)
