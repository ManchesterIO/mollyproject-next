Feature: Point of interest
  As a user
  I want to see information about a point of interest
  So I can make an informed decision about whether or not to visit there

  Scenario: Basic POI
    Given I am on the page for a point of interest
    Then I should be able to see the name of the Point of Interest
    And I should be able to see the category of the Point of Interest
    And I should see an attribution to the source of the data on this page

  Scenario: POI which has a location
    Given I am on the page for a point of interest which has a location
    Then I should be able to see a map
    And the map should have a marker indicating the point of interest
    And the map should be centred on the point of interest
    And the map should be at a zoom level showing a radius of about half a mile
    And I should see a link to find other points of interest nearby

  Scenario Outline: POI which has metadata
    Given I am on the page for a point of interest which has <metadata>
    Then I should be able to see <information>

  Examples:
    | metadata                      | information                                               |
    | a telephone number            | a link to dial the telephone number                       |
    | a website                     | a link to the website                                     |
