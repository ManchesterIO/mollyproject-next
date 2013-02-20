module MollyWorld
  include Weather

  PAGES = {
      :homepage => '/',
      :weather => '/weather/'
  }

  def visit_page(page)
    visit PAGES[page]
  end

end

World MollyWorld