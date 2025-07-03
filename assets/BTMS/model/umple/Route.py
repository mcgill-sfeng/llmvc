#PLEASE DO NOT EDIT THIS CODE
#This code was generated using the UMPLE 1.35.0.7523.c616a4dce modeling language!
# line 14 "model.ump"
# line 48 "model.ump"
import os
from datetime import date


class Route():
    routesByNumber = dict()
    #------------------------
    # STATIC VARIABLES
    #------------------------
    #------------------------
    # MEMBER VARIABLES
    #------------------------
    #Route Attributes
    #Route Associations
    #------------------------
    # CONSTRUCTOR
    #------------------------
    def __init__(self, aNumber, aBTMS):
        self._assignments = None
        self._bTMS = None
        self._number = None
        if not self.setNumber(aNumber) :
            raise RuntimeError ("Cannot create due to duplicate number. See https://manual.umple.org?RE003ViolationofUniqueness.html")
        didAddBTMS = self.setBTMS(aBTMS)
        if not didAddBTMS :
            raise RuntimeError ("Unable to create route due to bTMS. See https://manual.umple.org?RE002ViolationofAssociationMultiplicity.html")
        self._assignments = []

    #------------------------
    # INTERFACE
    #------------------------
    def setNumber(self, aNumber):
        wasSet = False
        anOldNumber = self.getNumber()
        if not (anOldNumber is None) and anOldNumber == aNumber :
            return True
        if Route.hasWithNumber(aNumber) :
            return wasSet
        self._number = aNumber
        wasSet = True
        if not (anOldNumber is None) :
            Route.routesByNumber.pop(anOldNumber)
        Route.routesByNumber[aNumber] = self
        return wasSet

    def getNumber(self):
        return self._number

    # Code from template attribute_GetUnique
    @staticmethod
    def getWithNumber(aNumber):
        return Route.routesByNumber.get(aNumber)

    # Code from template attribute_HasUnique
    @staticmethod
    def hasWithNumber(aNumber):
        return not (Route.getWithNumber(aNumber) is None)

    # Code from template association_GetOne
    def getBTMS(self):
        return self._bTMS

    # Code from template association_GetMany
    def getAssignment(self, index):
        aAssignment = self._assignments[index]
        return aAssignment

    def getAssignments(self):
        newAssignments = tuple(self._assignments)
        return newAssignments

    def numberOfAssignments(self):
        self._number = len(self._assignments)
        return self._number

    def hasAssignments(self):
        has = len(self._assignments) > 0
        return has

    def indexOfAssignment(self, aAssignment):
        index = (-1 if not aAssignment in self._assignments else self._assignments.index(aAssignment))
        return index

    # Code from template association_SetOneToMany
    def setBTMS(self, aBTMS):
        wasSet = False
        if aBTMS is None :
            return wasSet
        existingBTMS = self._bTMS
        self._bTMS = aBTMS
        if not (existingBTMS is None) and not existingBTMS == aBTMS :
            existingBTMS.removeRoute(self)
        self._bTMS.addRoute(self)
        wasSet = True
        return wasSet

    # Code from template association_MinimumNumberOfMethod
    @staticmethod
    def minimumNumberOfAssignments():
        return 0

    # Code from template association_AddManyToOne
    def addAssignment1(self, aDate, aBus, aBTMS):
        from assets.BTMS.model.umple.RouteAssignment import RouteAssignment
        return RouteAssignment(aDate, aBus, self, aBTMS)

    def addAssignment2(self, aAssignment):
        wasAdded = False
        if (aAssignment) in self._assignments :
            return False
        existingRoute = aAssignment.getRoute()
        isNewRoute = not (existingRoute is None) and not self == existingRoute
        if isNewRoute :
            aAssignment.setRoute(self)
        else :
            self._assignments.append(aAssignment)
        wasAdded = True
        return wasAdded

    def removeAssignment(self, aAssignment):
        wasRemoved = False
        #Unable to remove aAssignment, as it must always have a route
        if not self == aAssignment.getRoute() :
            self._assignments.pop(aAssignment)
            wasRemoved = True
        return wasRemoved

    # Code from template association_AddIndexControlFunctions
    def addAssignmentAt(self, aAssignment, index):
        wasAdded = False
        if self.addAssignment(aAssignment) :
            if index < 0 :
                index = 0
            if index > self.numberOfAssignments() :
                index = self.numberOfAssignments() - 1
            self._assignments.pop(aAssignment)
            self._assignments.insert(index, aAssignment)
            wasAdded = True
        return wasAdded

    def addOrMoveAssignmentAt(self, aAssignment, index):
        wasAdded = False
        if (aAssignment) in self._assignments :
            if index < 0 :
                index = 0
            if index > self.numberOfAssignments() :
                index = self.numberOfAssignments() - 1
            self._assignments.pop(aAssignment)
            self._assignments.insert(index, aAssignment)
            wasAdded = True
        else :
            wasAdded = self.addAssignmentAt(aAssignment, index)
        return wasAdded

    def delete(self):
        Route.routesByNumber.pop(self.getNumber())
        placeholderBTMS = self._bTMS
        self._bTMS = None
        if not (placeholderBTMS is None) :
            placeholderBTMS.removeRoute(self)
        i = len(self._assignments)
        while i > 0 :
            aAssignment = self._assignments[i - 1]
            aAssignment.delete()
            i -= 1

    def __str__(self):
        return str(super().__str__()) + "[" + "number" + ":" + str(self.getNumber()) + "]" + str(os.linesep) + "  " + "bTMS = " + ((format(id(self.getBTMS()), "x")) if not (self.getBTMS() is None) else "null")

    def addAssignment(self, *argv):
        from assets.BTMS.model.umple.BusVehicle import BusVehicle
        from assets.BTMS.model.umple.RouteAssignment import RouteAssignment
        from assets.BTMS.model.umple.BTMS import BTMS
        if len(argv) == 3 and isinstance(argv[0], date) and isinstance(argv[1], BusVehicle) and isinstance(argv[2], BTMS) :
            return self.addAssignment1(argv[0], argv[1], argv[2])
        if len(argv) == 1 and isinstance(argv[0], RouteAssignment) :
            return self.addAssignment2(argv[0])
        raise TypeError("No method matches provided parameters")