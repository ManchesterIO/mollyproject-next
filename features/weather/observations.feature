Feature: Weather Observations
  As a user
  I want to be able to see more in-depth weather observations for my local area
  So that I can make decisions with that information

  Scenario: Weather observation shows correct details
    Given I am on the weather page
    Then I should be able to see a one phrase summary of the current conditions
    And I should be able to see the current temperature
    And I should be able to see the current wind speed and direction
    And I should be able to see the current pressure
    And I should be able to see information about when and where this observation was made

  Scenario: Correct attribution is shown
    Given I am on the weather page
    Then I should be able to see some attribution of the observation source

  Scenario: Homepage widget shows summary only
    Given I am on the homepage
    Then I should be able to see a one phrase summary of the current conditions
    And I should not be able to see the current temperature
    And I should not be able to see the current wind speed and direction
    And I should not be able to see the current pressure
    And I should not be able to see information about when and where this observation was made