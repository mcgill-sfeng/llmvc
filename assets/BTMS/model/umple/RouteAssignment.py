#PLEASE DO NOT EDIT THIS CODE
#This code was generated using the UMPLE 1.35.0.7523.c616a4dce modeling language!
# line 18 "model.ump"
# line 53 "model.ump"
import os

class RouteAssignment():
    #------------------------
    # MEMBER VARIABLES
    #------------------------
    #RouteAssignment Attributes
    #RouteAssignment Associations
    #------------------------
    # CONSTRUCTOR
    #------------------------
    def __init__(self, aDate, aBus, aRoute, aBTMS):
        self._schedules = None
        self._bTMS = None
        self._route = None
        self._bus = None
        self._date = None
        self._date = aDate
        didAddBus = self.setBus(aBus)
        if not didAddBus :
            raise RuntimeError ("Unable to create assignment due to bus. See https://manual.umple.org?RE002ViolationofAssociationMultiplicity.html")
        didAddRoute = self.setRoute(aRoute)
        if not didAddRoute :
            raise RuntimeError ("Unable to create assignment due to route. See https://manual.umple.org?RE002ViolationofAssociationMultiplicity.html")
        didAddBTMS = self.setBTMS(aBTMS)
        if not didAddBTMS :
            raise RuntimeError ("Unable to create assignment due to bTMS. See https://manual.umple.org?RE002ViolationofAssociationMultiplicity.html")
        self._schedules = []

    #------------------------
    # INTERFACE
    #------------------------
    def setDate(self, aDate):
        wasSet = False
        self._date = aDate
        wasSet = True
        return wasSet

    def getDate(self):
        return self._date

    # Code from template association_GetOne
    def getBus(self):
        return self._bus

    # Code from template association_GetOne
    def getRoute(self):
        return self._route

    # Code from template association_GetOne
    def getBTMS(self):
        return self._bTMS

    # Code from template association_GetMany
    def getSchedule(self, index):
        aSchedule = self._schedules[index]
        return aSchedule

    def getSchedules(self):
        newSchedules = tuple(self._schedules)
        return newSchedules

    def numberOfSchedules(self):
        number = len(self._schedules)
        return number

    def hasSchedules(self):
        has = len(self._schedules) > 0
        return has

    def indexOfSchedule(self, aSchedule):
        index = (-1 if not aSchedule in self._schedules else self._schedules.index(aSchedule))
        return index

    # Code from template association_SetOneToMany
    def setBus(self, aBus):
        wasSet = False
        if aBus is None :
            return wasSet
        existingBus = self._bus
        self._bus = aBus
        if not (existingBus is None) and not existingBus == aBus :
            existingBus.removeAssignment(self)
        self._bus.addAssignment(self)
        wasSet = True
        return wasSet

    # Code from template association_SetOneToMany
    def setRoute(self, aRoute):
        wasSet = False
        if aRoute is None :
            return wasSet
        existingRoute = self._route
        self._route = aRoute
        if not (existingRoute is None) and not existingRoute == aRoute :
            existingRoute.removeAssignment(self)
        self._route.addAssignment(self)
        wasSet = True
        return wasSet

    # Code from template association_SetOneToMany
    def setBTMS(self, aBTMS):
        wasSet = False
        if aBTMS is None :
            return wasSet
        existingBTMS = self._bTMS
        self._bTMS = aBTMS
        if not (existingBTMS is None) and not existingBTMS == aBTMS :
            existingBTMS.removeAssignment(self)
        self._bTMS.addAssignment(self)
        wasSet = True
        return wasSet

    # Code from template association_MinimumNumberOfMethod
    @staticmethod
    def minimumNumberOfSchedules():
        return 0

    # Code from template association_AddManyToOne
    def addSchedule1(self, aShift, aDriver, aBTMS):
        from assets.BTMS.model.umple.DriverSchedule import DriverSchedule
        return DriverSchedule(aShift, aDriver, self, aBTMS)

    def addSchedule2(self, aSchedule):
        wasAdded = False
        if (aSchedule) in self._schedules :
            return False
        existingAssignment = aSchedule.getAssignment()
        isNewAssignment = not (existingAssignment is None) and not self == existingAssignment
        if isNewAssignment :
            aSchedule.setAssignment(self)
        else :
            self._schedules.append(aSchedule)
        wasAdded = True
        return wasAdded

    def removeSchedule(self, aSchedule):
        wasRemoved = False
        #Unable to remove aSchedule, as it must always have a assignment
        if not self == aSchedule.getAssignment() :
            self._schedules.pop(aSchedule)
            wasRemoved = True
        return wasRemoved

    # Code from template association_AddIndexControlFunctions
    def addScheduleAt(self, aSchedule, index):
        wasAdded = False
        if self.addSchedule(aSchedule) :
            if index < 0 :
                index = 0
            if index > self.numberOfSchedules() :
                index = self.numberOfSchedules() - 1
            self._schedules.pop(aSchedule)
            self._schedules.insert(index, aSchedule)
            wasAdded = True
        return wasAdded

    def addOrMoveScheduleAt(self, aSchedule, index):
        wasAdded = False
        if (aSchedule) in self._schedules :
            if index < 0 :
                index = 0
            if index > self.numberOfSchedules() :
                index = self.numberOfSchedules() - 1
            self._schedules.pop(aSchedule)
            self._schedules.insert(index, aSchedule)
            wasAdded = True
        else :
            wasAdded = self.addScheduleAt(aSchedule, index)
        return wasAdded

    def delete(self):
        placeholderBus = self._bus
        self._bus = None
        if not (placeholderBus is None) :
            placeholderBus.removeAssignment(self)
        placeholderRoute = self._route
        self._route = None
        if not (placeholderRoute is None) :
            placeholderRoute.removeAssignment(self)
        placeholderBTMS = self._bTMS
        self._bTMS = None
        if not (placeholderBTMS is None) :
            placeholderBTMS.removeAssignment(self)
        i = len(self._schedules)
        while i > 0 :
            aSchedule = self._schedules[i - 1]
            aSchedule.delete()
            i -= 1

    def __str__(self):
        return str(super().__str__()) + "[" + "]" + str(os.linesep) + "  " + "date" + "=" + str((((self.getDate().__str__().replaceAll("  ", "    ")) if not self.getDate() == self else "this") if not (self.getDate() is None) else "null")) + str(os.linesep) + "  " + "bus = " + str(((format(id(self.getBus()), "x")) if not (self.getBus() is None) else "null")) + str(os.linesep) + "  " + "route = " + str(((format(id(self.getRoute()), "x")) if not (self.getRoute() is None) else "null")) + str(os.linesep) + "  " + "bTMS = " + ((format(id(self.getBTMS()), "x")) if not (self.getBTMS() is None) else "null")

    def addSchedule(self, *argv):
        from assets.BTMS.model.umple.Driver import Driver
        from assets.BTMS.model.umple.DriverSchedule import DriverSchedule
        from assets.BTMS.model.umple.BTMS import BTMS
        if len(argv) == 3 and isinstance(argv[0], DriverSchedule.Shift) and isinstance(argv[1], Driver) and isinstance(argv[2], BTMS) :
            return self.addSchedule1(argv[0], argv[1], argv[2])
        if len(argv) == 1 and isinstance(argv[0], DriverSchedule) :
            return self.addSchedule2(argv[0])
        raise TypeError("No method matches provided parameters")





