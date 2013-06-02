class Map < Component

  def initialize(container)
    @id = container[:id]
  end

  def has_marker?(lat, lng)
    page.execute_script("var found=false;$('##{@id}').data('map').eachLayer(function(layer){ if (layer.getLatLng().equals(new L.LatLng(#{lat}, #{lng})) { found = true; }, this); return found;")
  end

  def has_centre?(lat, lng)
    page.execute_script("$('##{@id}').data('map').getCenter().equals(new L.LatLng(#{lat}, #{lng}))")
  end

  def zoom
    page.execute_script("$('##{@id}').data('map').getZoom()")
  end

end