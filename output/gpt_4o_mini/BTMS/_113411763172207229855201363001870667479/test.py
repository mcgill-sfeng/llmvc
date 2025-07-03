from datetime import date
from unittest.mock import patch

from assets.BTMS.model.umple import BusVehicle, Route, Driver
from output.gpt_4o_mini.BTMS._113411763172207229855201363001870667479.controller import BTMSController

MODEL_MODULE = 'assets.BTMS.model.umple'
TEST_MODULE = 'output.gpt_4o_mini.BTMS._113411763172207229855201363001870667479'

def test_create_driver_1():
    controller = BTMSController()
    Driver.driversByName.clear()
    try:
        controller.create_driver('John Doe')
    except ValueError:
        return False
    return len(controller.btms.getDrivers()) == 1

def test_create_driver_2():
    controller = BTMSController()
    Driver.driversByName.clear()
    try:
        controller.create_driver('')
    except Exception as e:
        if 'The name of a driver cannot be empty.' != str(e):
            print(
                f"Warning: Error message '{str(e)}' does not match expected message 'The name of a driver cannot be empty.'")
        return len(controller.btms.getDrivers()) == 0
    return False

def test_create_route_1():
    controller = BTMSController()
    Route.routesByNumber.clear()
    try:
        controller.create_route(3)
    except ValueError:
        return False
    return len(controller.btms.getRoutes()) == 1 and controller.btms.getRoute(0).getNumber() == 3

def test_create_route_2():
    controller = BTMSController()
    Route.routesByNumber.clear()
    try:
        controller.create_route(3)
        controller.create_route(3)
    except Exception as e:
        if 'A route with this number already exists. Please use a different number.' != str(e):
            print(
                f"Warning: Error message '{str(e)}' does not match expected message 'A route with this number already exists. Please use a different number.'")
        return len(controller.btms.getRoutes()) == 1
    return False

def test_create_route_3():
    controller = BTMSController()
    Route.routesByNumber.clear()
    try:
        controller.create_route(5)
    except ValueError:
        return False
    return len(controller.btms.getRoutes()) == 1 and controller.btms.getRoute(0).getNumber() == 5

def test_create_route_4():
    controller = BTMSController()
    Route.routesByNumber.clear()
    try:
        controller.create_route(10)
    except ValueError:
        return False
    return len(controller.btms.getRoutes()) == 1 and controller.btms.getRoute(0).getNumber() == 10

def test_create_route_5():
    controller = BTMSController()
    Route.routesByNumber.clear()
    try:
        controller.create_route(-2)
    except Exception as e:
        if 'The number of a route must be greater than zero.' != str(e):
            print(
                f"Warning: Error message '{str(e)}' does not match expected message 'The number of a route must be greater than zero.'")
        return len(controller.btms.getRoutes()) == 0
    return False

def test_create_route_6():
    controller = BTMSController()
    Route.routesByNumber.clear()
    try:
        controller.create_route(10000)
    except Exception as e:
        if 'The number of a route cannot be greater than 9999.' != str(e):
            print(
                f"Warning: Error message '{str(e)}' does not match expected message 'The number of a route cannot be greater than 9999.'")
        return len(controller.btms.getRoutes()) == 0
    return False

@patch('output.gpt_4o_mini.BTMS._113411763172207229855201363001870667479.controller.date')
def test_create_route_assignment_1(mock_datetime):
    mock_datetime.today.return_value = date(2021, 10, 7)
    controller = BTMSController()
    BusVehicle.busvehiclesByLicencePlate.clear()
    Route.routesByNumber.clear()
    vehicle = controller.btms.addVehicle('123456')
    controller.btms.addVehicle('654321')
    controller.btms.addRoute(101)
    try:
        controller.create_route_assignment('123456', 101, date(2021, 10, 8))
    except ValueError:
        return False
    return len(controller.btms.getAssignments()) == 1 and controller.btms.getAssignment(0).getBus().getLicencePlate() == '123456' and controller.btms.getAssignment(0).getRoute().getNumber() == 101 and controller.btms.getAssignment(0).getDate() == date(2021, 10, 8) and vehicle.getAssignment(0).getRoute().getNumber() == 101

@patch('output.gpt_4o_mini.BTMS._113411763172207229855201363001870667479.controller.date')
def test_create_route_assignment_2(mock_datetime):
    mock_datetime.today.return_value = date(2021, 10, 7)
    controller = BTMSController()
    BusVehicle.busvehiclesByLicencePlate.clear()
    Route.routesByNumber.clear()
    controller.btms.addVehicle('123456')
    controller.btms.addVehicle('654321')
    controller.btms.addRoute(101)
    try:
        controller.create_route_assignment('notreal', 101, date(2021, 10, 8))
    except Exception as e:
        if 'A bus must be specified for the assignment.' != str(e):
            print(f"Warning: Error message '{str(e)}' does not match expected message 'A bus must be specified for the assignment.'")
        return len(controller.btms.getAssignments()) == 0
    return False

@patch('output.gpt_4o_mini.BTMS._113411763172207229855201363001870667479.controller.date')
def test_create_route_assignment_3(mock_datetime):
    mock_datetime.today.return_value = date(2021, 10, 7)
    controller = BTMSController()
    BusVehicle.busvehiclesByLicencePlate.clear()
    Route.routesByNumber.clear()
    controller.btms.addVehicle('123456')
    controller.btms.addVehicle('654321')
    controller.btms.addRoute(101)
    try:
        controller.create_route_assignment('123456', 201, date(2021, 10, 8))
    except Exception as e:
        if 'A route must be specified for the assignment.' != str(e):
            print(f"Warning: Error message '{str(e)}' does not match expected message 'A route must be specified for the assignment.'")
        return len(controller.btms.getAssignments()) == 0
    return False

@patch('output.gpt_4o_mini.BTMS._113411763172207229855201363001870667479.controller.date')
def test_create_route_assignment_4(mock_datetime):
    mock_datetime.today.return_value = date(2021, 10, 7)
    controller = BTMSController()
    BusVehicle.busvehiclesByLicencePlate.clear()
    Route.routesByNumber.clear()
    controller.btms.addVehicle('123456')
    controller.btms.addVehicle('654321')
    controller.btms.addRoute(101)
    try:
        controller.create_route_assignment('654321', 101, date(2023, 10, 8))
    except Exception as e:
        if 'The date must be within a year from today.' != str(e):
            print(f"Warning: Error message '{str(e)}' does not match expected message 'The date must be within a year from today.'")
        return len(controller.btms.getAssignments()) == 0
    return False

if __name__ == '__main__':
    tests = [
        test_create_driver_1,
        test_create_driver_2,
        test_create_route_1,
        test_create_route_2,
        test_create_route_3,
        test_create_route_4,
        test_create_route_5,
        test_create_route_6,
        test_create_route_assignment_1,
        test_create_route_assignment_2,
        test_create_route_assignment_3,
        test_create_route_assignment_4
    ]

    pass_count = 0

    for i, test in enumerate(tests, 1):
        try:
            result = test()
            pass_count += 1 if result else 0
            print(f'Test {i}: {"Passed" if result else "Failed"}')
        except Exception as e:
            print(f'Test {i}: Failed with exception: {e}')

    print(f'Total Passed: {pass_count}/{len(tests)}')


