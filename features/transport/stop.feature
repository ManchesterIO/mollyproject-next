Feature: Stop information
  As a public transport user
  I want to see detailed information about a stop or station
  So I can monitor departures and arrival from it

  Scenario: Page widgets
    Given I am on a stop information page
    Then I should see a map of the stop's location
    And I should see a list of any other stops which this stop interchanges with
    And I should see a link to search nearby points of interest
    And I should see the current departure information for this stop
    And I should see a tab to switch to arrival information for this stop
    And I should see a tab to switch to destination information for this stop
    And I should see a tab to switch to route information for this stop
    And I should see information about the facilities of this stop
    And I should see about stop specific announcements

  Scenario: Page widgets for a stop on a rapid transit network
    Given I am on a stop information page for a stop which is part of a rapid transit network
    Then I should see a summary of the state of the rapid transit network

  Scenario: Stop which has no scheduled journeys
  Scenario: Stop which has platforms/bays
  Scenario: Interchange
  Scenario: Departure auto-update
  Scenario: Arrivals tab
  Scenario: Destinations tab
  Scenario: Routes tab
  Scenario: Route timetable
