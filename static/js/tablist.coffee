$ ->

  onItemClick = (evt) ->
    $this = $(this)
    $this.parent().find('.active').removeClass('active')
    $this.addClass('active')
    # Get the original item element
    $content = $this.data('content')
    # Hide all other original list elements
    $content.parent().find('> li').hide()
    # Show the item content
    $content.show()


  createTab = ($el) ->
    # Hide the original element
    $el.addClass('tablist-content')
    # Create the new list element
    $ul = $('<ul>').addClass('tablist')
    # Get all original list items
    $el_li = $el.find('li')
    li_width = ($el.parent().width() / $el_li.length)
    $el_li.each () ->
      $this = $(this)
      # Hide the original item
      $this.hide()
      # Create the new list item with the header from original list item
      $li = $('<li>').append $this.find('blockquote > h1').contents()
      # Set the correct width to all items be inline
      $ul.append $li.css(width: li_width)
      # Set reference to the original item
      $li.data('content', $this)
      # Bind the click event to display the original item
      $li.click onItemClick
    $el.before $ul


  $('#equipe > ul, #principios > ul').each () ->
    createTab($(this));

