Feature: Point of interest search
  As a user
  I want to be able to find a point of interest
  So I can decide to use it's services

  Scenario: Search by category
    Given I am on the nearby search page
    Then I should be able to see a list of categories which have nearby points of interest
    And I should be able to see a list of amenities which are nearby
    And each category should show how many of those points of interest are nearby

  Scenario Outline: Filter by category/amenity
    Given I am on the nearby search page
    When I select a <criteria> from the <criteria> list
    Then I should be taken to the filtered list of points of interest for that <criteria>

  Examples:
    | criteria |
    | category |
    | amenity  |

  Scenario: Search by location
  Scenario: Search by name
  Scenario: Single result
  Scenario: No results
  Scenario: Multiple results