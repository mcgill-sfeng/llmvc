#PLEASE DO NOT EDIT THIS CODE
#This code was generated using the UMPLE 1.35.0.7523.c616a4dce modeling language!
# line 24 "model.ump"
# line 58 "model.ump"
import os

class Driver():
    driversByName = dict()
    #------------------------
    # STATIC VARIABLES
    #------------------------
    #------------------------
    # MEMBER VARIABLES
    #------------------------
    #Driver Attributes
    #Driver Associations
    #------------------------
    # CONSTRUCTOR
    #------------------------
    def __init__(self, aName, aBTMS):
        self._schedules = None
        self._bTMS = None
        self._name = None
        if not self.setName(aName) :
            raise RuntimeError ("Cannot create due to duplicate name. See https://manual.umple.org?RE003ViolationofUniqueness.html")
        didAddBTMS = self.setBTMS(aBTMS)
        if not didAddBTMS :
            raise RuntimeError ("Unable to create driver due to bTMS. See https://manual.umple.org?RE002ViolationofAssociationMultiplicity.html")
        self._schedules = []

    #------------------------
    # INTERFACE
    #------------------------
    def setName(self, aName):
        wasSet = False
        anOldName = self.getName()
        if not (anOldName is None) and anOldName == aName :
            return True
        if Driver.hasWithName(aName) :
            return wasSet
        self._name = aName
        wasSet = True
        if not (anOldName is None) :
            Driver.driversByName.pop(anOldName)
        Driver.driversByName[aName] = self
        return wasSet

    def getName(self):
        return self._name

    # Code from template attribute_GetUnique
    @staticmethod
    def getWithName(aName):
        return Driver.driversByName.get(aName)

    # Code from template attribute_HasUnique
    @staticmethod
    def hasWithName(aName):
        return not (Driver.getWithName(aName) is None)

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
    def setBTMS(self, aBTMS):
        wasSet = False
        if aBTMS is None :
            return wasSet
        existingBTMS = self._bTMS
        self._bTMS = aBTMS
        if not (existingBTMS is None) and not existingBTMS == aBTMS :
            existingBTMS.removeDriver(self)
        self._bTMS.addDriver(self)
        wasSet = True
        return wasSet

    # Code from template association_MinimumNumberOfMethod
    @staticmethod
    def minimumNumberOfSchedules():
        return 0

    # Code from template association_AddManyToOne
    def addSchedule1(self, aShift, aAssignment, aBTMS):
        from assets.BTMS.model.umple.DriverSchedule import DriverSchedule
        return DriverSchedule(aShift, self, aAssignment, aBTMS)

    def addSchedule2(self, aSchedule):
        wasAdded = False
        if (aSchedule) in self._schedules :
            return False
        existingDriver = aSchedule.getDriver()
        isNewDriver = not (existingDriver is None) and not self == existingDriver
        if isNewDriver :
            aSchedule.setDriver(self)
        else :
            self._schedules.append(aSchedule)
        wasAdded = True
        return wasAdded

    def removeSchedule(self, aSchedule):
        wasRemoved = False
        #Unable to remove aSchedule, as it must always have a driver
        if not self == aSchedule.getDriver() :
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
        Driver.driversByName.pop(self.getName())
        placeholderBTMS = self._bTMS
        self._bTMS = None
        if not (placeholderBTMS is None) :
            placeholderBTMS.removeDriver(self)
        i = len(self._schedules)
        while i > 0 :
            aSchedule = self._schedules[i - 1]
            aSchedule.delete()
            i -= 1

    def __str__(self):
        return str(super().__str__()) + "[" + "name" + ":" + str(self.getName()) + "]" + str(os.linesep) + "  " + "bTMS = " + ((format(id(self.getBTMS()), "x")) if not (self.getBTMS() is None) else "null")

    def addSchedule(self, *argv):
        from assets.BTMS.model.umple.DriverSchedule import DriverSchedule
        from assets.BTMS.model.umple.BTMS import BTMS
        from assets.BTMS.model.umple.RouteAssignment import RouteAssignment
        if len(argv) == 3 and isinstance(argv[0], DriverSchedule.Shift) and isinstance(argv[1], RouteAssignment) and isinstance(argv[2], BTMS) :
            return self.addSchedule1(argv[0], argv[1], argv[2])
        if len(argv) == 1 and isinstance(argv[0], DriverSchedule) :
            return self.addSchedule2(argv[0])
        raise TypeError("No method matches provided parameters")





