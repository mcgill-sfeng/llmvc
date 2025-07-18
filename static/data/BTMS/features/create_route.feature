Feature: Create route

  Background:
    Given there is a BTMS system

  Scenario: Create a new route
    When a new route with number 3 is created
    Then the BTMS system has a new route
    Then this new route has the number 3
    Then the system shall not throw an error
    Then the number of routes in the BTMS shall be 1
    Then this new route has the number 3

  Scenario: Create two routes with the same number
    When a new route with number 3 is created
    When a new route with number 3 is created
    Then the system shall throw with error message "A route with this number already exists. Please use a different number."
    Then the number of routes in the BTMS shall be 1

  Scenario Outline: Create a new route with scenario outline
    When a new route with number <number> is created
    Then the system shall not throw an error
    Then the BTMS system has a new route
    Then the number of routes in the BTMS shall be 1
    Then this new route has the number <number>

    Examples:
      | number |
      |      5 |
      |     10 |

  Scenario Outline: Try creating a new route with invalid number
    When a new route with number <number> is created
    Then the system shall throw with error message "<errormsg>"
    Then the number of routes in the BTMS shall be 0

    Examples:
      | number | errormsg                                           |
      |     -2 | The number of a route must be greater than zero.   |
      |  10000 | The number of a route cannot be greater than 9999. |