Given /^I am on the weather page$/ do
  visit_page :weather
end

Then /^I should be able to see a one phrase summary of the current conditions$/ do
  weather_observation.should have_one_phrase_summary
end

Then /^I should be able to see the current temperature$/ do
  weather_observation.should have_temperature
end

Then /^I should not be able to see the current temperature$/ do
  weather_observation.should_not have_temperature
end

Then /^I should be able to see the current wind speed and direction/ do
  weather_observation.should have_wind_speed_and_direction
end

Then /^I should not be able to see the current wind speed and direction/ do
  weather_observation.should_not have_wind_speed_and_direction
end

Then /^I should be able to see the current pressure$/ do
  weather_observation.should have_pressure
end

Then /^I should not be able to see the current pressure$/ do
  weather_observation.should_not have_pressure
end

Then /^I should be able to see information about when and where this observation was made$/ do
  weather_observation.should have_observation_details
end

Then /^I should not be able to see information about when and where this observation was made$/ do
  weather_observation.should_not have_observation_details
end

Then /^I should be able to see some attribution of the observation source$/ do
  weather_observation.should have_attribution
end
