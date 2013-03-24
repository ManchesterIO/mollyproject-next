Feature: Transport Homepage widgets
  As a user of public transport
  I want to be able to quickly get to currently running information about public transport services
  So I can make transport decisions
  And I have a reason to come back to the application

  Scenario: Homepage has stop search box
    Given I am on the homepage
    Then I should see a find stop icon
    And I should see a stop search box
    And I should see a find nearby button

  Scenario: Find stop by ID
    Given I am on the homepage
    When I enter the identifying code for that stop
    Then I should be taken to more in-depth information about that stop

  Scenario: Find stop by ID but none matches
    Given I am on the homepage
    And I enter an identifying code for a stop which does not exist
    Then I should shown an error message saying that no stop matching that code exists

  Scenario: Find stop by longitude and latitude when accuracy is imprecise and stops nearby
    Given I am on the homepage
    And my geolocation accuracy is over 250m
    And there are stops within 250m of me
    When I select the find nearby button
    Then I should see all stops within the 250m radius

  Scenario: Find stop by longitude and latitude when accuracy is imprecise but no stops nearby
    Given I am on the homepage
    And my geolocation accuracy is over 250m
    And there are no stops within 250m of me
    When I select the find nearby button
    Then I should see the closest 10 stops

  Scenario: Find stop by longitude and latitude when accuracy is precise and stops nearby
    Given I am on the homepage
    And my geolocation accuracy is under 100m
    And there are stops within 100m of me
    When I select the find nearby button
    Then I should see all stops within the 100m radius

  Scenario: Find stop by longitude and latitude when accuracy is precise but no stops nearby
    Given I am on the homepage
    And my geolocation accuracy is under 100m
    And there are no stops within 100m of me
    When I select the find nearby button
    Then I should see the closest 10 stops

  Scenario: Find stop by longitude and latitude when no geolocation is available
    Given I am on the homepage
    And my geolocated position is unavailable
    When I select the find nearby button
    Then I should see a message telling me that this feature is unavailable without geolocation

  Scenario: Find stop by latitude and longitude when geolocation is available but not yet determined
    Given I am on the homepage
    And my geolocated position is unavailable
    When I select the find nearby button
    Then I should see see an indicator that my position is being determined
    When my position is determined
    Then I should see the closest 10 stops

  Scenario: Find stop by latitude and longitude when geolocation is available but not determinable
    Given I am on the homepage
    And my geolocated position is unavailable
    When I select the find nearby button
    Then I should see see an indicator that my position is being determined
    When I wait 30 seconds
    Then I should see a message indicating my position should not be determined


  Scenario: Find stop by geolocation
  Scenario: Find stop by stop name
  Scenario: Rapid transit status dashboard
  Scenario: Rail station when nearby
  Scenario: Rail station when not nearby
  Scenario: Rail station when closest is non-major station
