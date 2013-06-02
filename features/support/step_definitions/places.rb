Given(/^I am on the page for a point of interest(?: which has a (?:location|telephone number))?$/) do
  visit_page :poi
end

Then(/^I should be able to see the name of the Point of Interest$/) do
  poi.should have_name
end

When(/^I should be able to see the category of the Point of Interest$/) do
  poi.should have_category
end

When(/^I should see an attribution to the source of the data on this page$/) do
  poi.should have_attribution
end

Then(/^I should be able to see a map$/) do
  poi.should have_map
end

Then(/^the map should have a marker indicating the point of interest$/) do
  poi.map.should have_marker('53.4590369', '-2.2273054')
end

Then(/^the map should be centred on the point of interest$/) do
  poi.map.should have_centre('53.4590369', '-2.2273054')
end

Then(/^the map should be at a zoom level showing a radius of about half a mile$/) do
  poi.map.zoom.should == 12
end
