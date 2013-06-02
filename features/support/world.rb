module MollyWorld
  include Places
  include Weather

  PAGES = {
      :homepage => '/',
      :weather => '/weather/',
      :poi => '/places/osm:N258869417/'
  }

  def visit_page(page)
    visit PAGES[page]
  end

end

World MollyWorld