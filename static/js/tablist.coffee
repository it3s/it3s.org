$ ->

  fragments = {}

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
    window.location.hash = $this.data('fragment') if $this.data('fragment')


  createTab = ($el, clickable=true) ->
    # Hide the original element
    $el.addClass('tablist-content')
    # Create the new list element
    $ul = $('<ul>').addClass('tablist')
    # Get all original list items
    $el_li = $el.find('> li')
    li_width = ($el.parent().width() / $el_li.length)
    el_minHeight = 0

    $el_li.each (index) ->
      $this = $(this)
      $title = $this.find('blockquote > h1').remove()
      # Create the new list item with the header from original list item
      $li = $('<li>').append $title.contents()
      # Set the correct width to all items be inline
      $ul.append $li.css(width: li_width)
      # Use url fragment
      fragment = $title.attr('data-url')
      if fragment
        $li.data('fragment', "##{fragment}")
        fragments["##{fragment}"] = $li
      # Set reference to the original item
      $li.data('content', $this)
      $li.addClass 'clickable' if clickable
      $li.data('clickFunction', onItemClick)
      # Bind the click event to display the original item
      $li.click onItemClick if clickable and not fragment
      $li.click( -> window.location.hash = fragment ) if clickable and fragment
      ## Stop footer dance
      #el_minHeight = parseInt($el.css('min-height'), 10) or 0
      #this_height = $this.height()
      #$el.css('min-height', (if el_minHeight > this_height then el_minHeight else this_height))
      # Hide the original item
      $this.hide()
      # Start showing the first item
      $li.click() if index is 0

    #$el.css('min-height', el_minHeight + 35)
    $el.before $ul

  $(window).bind 'hashchange', ->
    fragment = window.location.hash
    $li = fragments[fragment]
    clickFunction = $li.data('clickFunction')
    clickFunction.apply($li)


  $('''#equipe > ul:first, #parceiros-financeiros > ul, #metodologia-cenario > ul''').each () ->
    createTab($(this))

  $('''#principios > ul, #parceiros-divulgacao > ul, #parceiros-tecnicos > ul''').each () ->
    createTab($(this), false)
