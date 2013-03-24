Feature: Points of Interest homepage widgets

  Scenario: Show nearby
    Given I am on the homepage
    Then I should see a widget to Show Nearby POIs

  Scenario: Nearby POIs are sorted by category
    Given I am on the homepage
    And my geolocated position is available
    When I select the Show Nearby POIs widget
    Then I should see a list of categories with nearby POIs
    And on each category I should see the number of POIs found nearby
    When I select a category
    Then I should see a list of POIs in that category which are nearby

  Scenario: POI list
    Given I can see a list of POIs
    Then each POI shows a title and subheading
    And each POI which has opening times shows a badge indicating whether or not it is open
    And each POI which is closer than the current level of geolocation accuracy indicates that it is nearby
    And each POI which is further away than the current level of geolocation accuracy indicates distance and direction

  Scenario: Find nearby when geolocation is unavailable
    Given I am on the homepage
    And my geolocated position is unavailable
    When I select the Show Nearby POIs widget
    Then I should see a message telling me that this feature is unavailable without geolocation

  Scenario: Find nearby when geolocation is available but not yet determined
    Given I am on the homepage
    And my geolocated position is unavailable
    When I select the Show Nearby POIs widget
    Then I should see see an indicator that my position is being determined
    When my position is determined
    Then I should see a list of categories with nearby POIs

  Scenario: Find nearby when geolocation is available but not determinable
    Given I am on the homepage
    And my geolocated position is unavailable
    When I select the Show Nearby POIs widget
    Then I should see see an indicator that my position is being determined
    When I wait 30 seconds
    Then I should see a message indicating my position should not be determined

  Scenario: Find place
    Given I am on the homepage
    Then I should see a widget to Find Place
    When I enter a location name
    And I select the search icon
    Then I should be taken to the search results page for that search term
