module Places

  class PointOfInterest < Component

    def has_name?
      container.has_css? 'h1'
    end

    def has_category?
      container.has_css? '.category'
    end

    def has_attribution?
      container.has_css? '.attribution'
    end

    def has_map?
      container.has_css? '.leaflet-container'
    end

    def has_telephone_number?
      container.has_css? '.telephone-number'
    end

    def map
      Map.new container.find('.leaflet-container')
    end

    private

    def container
      find('article')
    end

  end

  def poi
    PointOfInterest.new
  end

end