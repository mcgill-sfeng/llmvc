Feature: Route Assignment

  Background:
    Given there is a BTMS system
    Given the current system date is "2021-10-07"
    Given the following bus vehicles exist in the system
      | licencePlate | inRepairShop |
      |       123456 | false        |
      |       654321 | true         |
    Given the following routes exist in the system
      | number |
      |    101 |

  Scenario Outline: Assign bus vehicles successfully
    When vehicle "<vehicle>" is assigned to route "<route>" on date "<date>"
    Then the system shall not throw an error
    Then the number of assignments in the BTMS shall be 1
    Then this new assignment shall have the vehicle with licence plate "<vehicle>"
    Then this new assignment shall have the route with number "<route>"
    Then this new assignment shall have the date "<date>"
    Then vehicle "<vehicle>" shall have an assignment to route "<route>" on date "<date>"

    Examples:
      | vehicle | route | date       |
      |  123456 |   101 | 2021-10-08 |

  Scenario Outline: Assign bus vehicles with invalid inputs
    When vehicle "<vehicle>" is assigned to route "<route>" on date "<date>"
    Then the system shall throw with error message "<errormsg>"
    Then the number of assignments in the BTMS shall be 0
    Then vehicle "<vehicle>" shall not have an assignment to route "<route>" on date "<date>"

    Examples:
      | vehicle | route | date       | errormsg                                      |
      | notreal |   101 | 2021-10-08 | A bus must be specified for the assignment.   |
      |  123456 |   201 | 2021-10-08 | A route must be specified for the assignment. |
      |  654321 |   101 | 2023-10-08 | The date must be within a year from today.    |