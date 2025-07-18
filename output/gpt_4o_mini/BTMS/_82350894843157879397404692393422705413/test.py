from datetime import date
from unittest.mock import patch
from pyecore.ecore import EDate

from assets.BTMS.model.ecore import BusVehicle, Route
from output.gpt_4o_mini.BTMS._82350894843157879397404692393422705413.controller import BTMSController

MODEL_MODULE = 'assets.BTMS.model.ecore'
TEST_MODULE = 'output.gpt_4o_mini.BTMS._82350894843157879397404692393422705413'

def test_create_driver_1():
    controller = BTMSController()
    try:
        controller.create_driver('John Doe')
    except ValueError:
        return False
    return len(controller.btms.drivers) == 1

def test_create_driver_2():
    controller = BTMSController()
    try:
        controller.create_driver('')
    except Exception as e:
        if 'The name of a driver cannot be empty.' != str(e):
            print(f"Warning: Error message '{str(e)}' does not match expected message 'The name of a driver cannot be empty.'")
        return len(controller.btms.drivers) == 0
    return False

def test_create_route_1():
    controller = BTMSController()
    try:
        controller.create_route(3)
    except ValueError:
        return False
    return len(controller.btms.routes) == 1 and controller.btms.routes[0].number == 3

def test_create_route_2():
    controller = BTMSController()
    try:
        controller.create_route(3)
        controller.create_route(3)
    except Exception as e:
        if 'A route with this number already exists. Please use a different number.' != str(e):
            print(f"Warning: Error message '{str(e)}' does not match expected message 'A route with this number already exists. Please use a different number.'")
        return len(controller.btms.routes) == 1
    return False

def test_create_route_3():
    controller = BTMSController()
    try:
        controller.create_route(5)
    except ValueError:
        return False
    return len(controller.btms.routes) == 1 and controller.btms.routes[0].number == 5

def test_create_route_4():
    controller = BTMSController()
    try:
        controller.create_route(10)
    except ValueError:
        return False
    return len(controller.btms.routes) == 1 and controller.btms.routes[0].number == 10

def test_create_route_5():
    controller = BTMSController()
    try:
        controller.create_route(-2)
    except Exception as e:
        if 'The number of a route must be greater than zero.' != str(e):
            print(f"Warning: Error message '{str(e)}' does not match expected message 'The number of a route must be greater than zero.'")
        return len(controller.btms.routes) == 0
    return False

def test_create_route_6():
    controller = BTMSController()
    try:
        controller.create_route(10000)
    except Exception as e:
        if 'The number of a route cannot be greater than 9999.' != str(e):
            print(f"Warning: Error message '{str(e)}' does not match expected message 'The number of a route cannot be greater than 9999.'")
        return len(controller.btms.routes) == 0
    return False

@patch('output.gpt_4o_mini.BTMS._82350894843157879397404692393422705413.controller.date')
def test_create_route_assignment_1(mock_datetime):
    mock_datetime.today.return_value = date(2021, 10, 7)
    controller = BTMSController()
    controller.btms.vehicles.append(BusVehicle(licencePlate='123456'))
    controller.btms.vehicles.append(BusVehicle(licencePlate='654321'))
    controller.btms.routes.append(Route(number=101))
    try:
        controller.create_route_assignment('123456', 101, date(2021, 10, 8))
    except ValueError:
        return False
    vehicle = next(v for v in controller.btms.vehicles if v.licencePlate == '123456')
    return len(controller.btms.assignments) == 1 and controller.btms.assignments[0].bus == vehicle and controller.btms.assignments[0].route.number == 101 and controller.btms.assignments[0].date == EDate.from_string(date(2021, 10, 8).strftime('%Y-%m-%dT%H:%M:%S.%f%z'))

@patch('output.gpt_4o_mini.BTMS._82350894843157879397404692393422705413.controller.date')
def test_create_route_assignment_2(mock_datetime):
    mock_datetime.today.return_value = date(2021, 10, 7)
    controller = BTMSController()
    controller.btms.vehicles.append(BusVehicle(licencePlate='123456'))
    controller.btms.vehicles.append(BusVehicle(licencePlate='654321'))
    route = Route(number=101)
    controller.btms.routes.append(route)
    try:
        controller.create_route_assignment('notreal', 101, date(2021, 10, 8))
    except Exception as e:
        if 'A bus must be specified for the assignment.' != str(e):
            print(f"Warning: Error message '{str(e)}' does not match expected message 'A bus must be specified for the assignment.'")
        return len(controller.btms.assignments) == 0
    return False

@patch('output.gpt_4o_mini.BTMS._82350894843157879397404692393422705413.controller.date')
def test_create_route_assignment_3(mock_datetime):
    mock_datetime.today.return_value = date(2021, 10, 7)
    controller = BTMSController()
    controller.btms.vehicles.append(BusVehicle(licencePlate='123456'))
    controller.btms.vehicles.append(BusVehicle(licencePlate='654321'))
    try:
        controller.create_route_assignment('123456', 201, date(2021, 10, 8))
    except Exception as e:
        if 'A route must be specified for the assignment.' != str(e):
            print(
                f"Warning: Error message '{str(e)}' does not match expected message 'A route must be specified for the assignment.'")
        return len(controller.btms.assignments) == 0
    return False

@patch('output.gpt_4o_mini.BTMS._82350894843157879397404692393422705413.controller.date')
def test_create_route_assignment_4(mock_datetime):
    mock_datetime.today.return_value = date(2021, 10, 7)
    controller = BTMSController()
    controller.btms.vehicles.append(BusVehicle(licencePlate='123456'))
    controller.btms.vehicles.append(BusVehicle(licencePlate='654321'))
    route = Route(number=101)
    controller.btms.routes.append(route)
    try:
        controller.create_route_assignment('654321', 101, date(2023, 10, 8))
    except Exception as e:
        if 'The date must be within a year from today.' != str(e):
            print(
                f"Warning: Error message '{str(e)}' does not match expected message 'The date must be within a year from today.'")
        return len(controller.btms.assignments) == 0
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


