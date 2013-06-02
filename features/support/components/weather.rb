module Weather

  class WeatherObservation < Component

    def container
      find('.weather-observation')
    end

    def has_one_phrase_summary?
      container.has_css? '.weather-summary'
    end

    def has_temperature?
      weather_detail_present? 'Temperature'
    end

    def has_wind_speed_and_direction?
      weather_detail_present? 'Wind'
    end

    def has_pressure?
      weather_detail_present? 'Pressure'
    end

    def has_observation_details?
      container.has_css? 'aside.observation-details'
    end

    def has_attribution?
      container.has_css? '.attribution'
    end

    private

    def weather_detail_present?(label)
      container.has_xpath? "./div[@class='weather-detail']/dl/dt[text()='#{label}']"
    end

  end

  def weather_observation
    WeatherObservation.new
  end

end