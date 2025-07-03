from pyecore.ecore import *

class DriverSchedule(EObject, metaclass=MetaEClass):
    Shift = EEnum('Shift', literals=['Morning', 'Afternoon', 'Night'])

    shift = EAttribute(eType=Shift, unique=True, derived=False, changeable=True)
    driver = EReference(ordered=True, unique=True, containment=False, derived=False)
    assignment = EReference(ordered=True, unique=True, containment=False, derived=False)

    def __init__(self, *, shift=None, driver=None, assignment=None):
        # if kwargs:
        #    raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if shift is not None:
            self.shift = shift

        if driver is not None:
            self.driver = driver

        if assignment is not None:
            self.assignment = assignment
