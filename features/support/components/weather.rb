module Weather

  class WeatherObservation
    include Capybara::DSL

    def container
      find('.weather-observation')
    end

    def has_one_phrase_summary?
      selector_present?(:css, '.weather-summary')
    end

    def has_temperature?
      weather_detail_present?('Temperature')
    end

    def has_wind_speed_and_direction?
      weather_detail_present?('Wind')
    end

    def has_pressure?
      weather_detail_present?('Pressure')
    end

    def has_observation_details?
      selector_present?(:css, 'aside.observation-details')
    end

    def has_attribution?
      selector_present?(:css, '.attribution')
    end

    private

    def weather_detail_present?(label)
      selector_present?(:xpath, "./div[@class='weather-detail']/dl/dt[text()='#{label}']")
    end

    def selector_present?(selector_type, selector)
      not container.first(selector_type, selector).nil?
    end

  end

  def weather_observation
    WeatherObservation.new
  end

end