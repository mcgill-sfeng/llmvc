from pyecore.ecore import *


class Route(EObject, metaclass=MetaEClass):

    number = EAttribute(eType=EIntegerObject, unique=True, derived=False, changeable=True)
    assignments = EReference(ordered=True, unique=True, containment=False, derived=False, upper=-1)

    def __init__(self, *, number=None, assignments=None):
        # if kwargs:
        #    raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if number is not None:
            self.number = number

        if assignments:
            self.assignments.extend(assignments)
