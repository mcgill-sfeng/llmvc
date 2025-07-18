from functools import partial
import pyecore.ecore as Ecore
from pyecore.ecore import *
from .BTMS import BTMS
from .BusVehicle import BusVehicle
from .Driver import Driver
from .DriverSchedule import DriverSchedule
from .Route import Route
from .RouteAssignment import RouteAssignment

name = 'btms'
nsURI = 'http://www.example.org/btms'
nsPrefix = 'btms'
eClass = EPackage(name=name, nsURI=nsURI, nsPrefix=nsPrefix)

eClassifiers = {}
getEClassifier = partial(Ecore.getEClassifier, searchspace=eClassifiers)

__all__ = ['BTMS', 'BusVehicle', 'Route', 'RouteAssignment', 'Driver', 'DriverSchedule']

eSubpackages = []
eSuperPackage = None

BTMS.vehicles.eType = BusVehicle
BTMS.routes.eType = Route
BTMS.assignments.eType = RouteAssignment
BTMS.drivers.eType = Driver
BTMS.schedules.eType = DriverSchedule
BusVehicle.assignments.eType = RouteAssignment
Route.assignments.eType = RouteAssignment
RouteAssignment.bus.eType = BusVehicle
RouteAssignment.route.eType = Route
RouteAssignment.schedules.eType = DriverSchedule
Driver.schedules.eType = DriverSchedule
DriverSchedule.Shift.eType = DriverSchedule.Shift
DriverSchedule.driver.eType = Driver
DriverSchedule.assignment.eType = RouteAssignment

for classif in eClassifiers.values():
    eClass.eClassifiers.append(classif.eClass)

for subpack in eSubpackages:
    eClass.eSubpackages.append(subpack.eClass)
