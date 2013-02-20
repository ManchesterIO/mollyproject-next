require 'capybara/cucumber'
require 'capybara/poltergeist'
require 'capybara/rspec'

Capybara.app_host = 'http://192.168.33.10:8002'
Capybara.default_driver = :poltergeist