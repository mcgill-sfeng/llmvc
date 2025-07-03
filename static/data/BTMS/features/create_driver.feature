Feature: Create driver

  Background:
    Given there is a BTMS system

  Scenario: Creating a new driver
    When a driver with name "John Doe" is created
    Then the system shall not throw an error
    Then the number of drivers in the BTMS shall be 1

  Scenario: Creating a driver with invalid name
    When a driver with name "" is created
    Then the system shall throw with error message "The name of a driver cannot be empty."
    Then the number of drivers in the BTMS shall be 0