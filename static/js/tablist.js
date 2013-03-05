(function() {

  $(function() {
    var createTab, fragments, onItemClick;
    fragments = {};
    onItemClick = function(evt) {
      var $content, $this;
      $this = $(this);
      $this.parent().find('.active').removeClass('active');
      $this.addClass('active');
      $content = $this.data('content');
      $content.parent().find('> li').hide();
      $content.show();
      console.log('---->', window.location.hash, $this.data('fragment'));
      if ($this.data('fragment')) {
        return window.location.hash = $this.data('fragment');
      }
    };
    createTab = function($el, clickable) {
      var $el_li, $ul, el_minHeight, li_width;
      if (clickable == null) clickable = true;
      $el.addClass('tablist-content');
      $ul = $('<ul>').addClass('tablist');
      $el_li = $el.find('> li');
      li_width = $el.parent().width() / $el_li.length;
      el_minHeight = 0;
      $el_li.each(function(index) {
        var $li, $this, $title, dataUrl, fragment, _i, _len, _ref;
        $this = $(this);
        $title = $this.find('blockquote > h1').remove();
        $li = $('<li>').append($title.contents());
        $li.attr('id', $title.attr('id'));
        $ul.append($li.css({
          width: li_width
        }));
        dataUrl = $title.attr('data-url');
        _ref = dataUrl.split('|');
        for (_i = 0, _len = _ref.length; _i < _len; _i++) {
          fragment = _ref[_i];
          if (fragment) {
            if (!$li.data('fragment')) $li.data('fragment', "#" + fragment);
            fragments["#" + fragment] = $li;
            if (index === 0) fragments[''] = $li;
          }
        }
        $li.data('content', $this);
        if (clickable) $li.addClass('clickable');
        $li.data('clickFunction', onItemClick);
        if (clickable && !fragment) $li.click(onItemClick);
        if (clickable && fragment) {
          $li.click(function() {
            return window.location.hash = $li.data('fragment');
          });
        }
        return $this.hide();
      });
      return $el.before($ul);
    };
    $(window).bind('hashchange', function() {
      var $li, clickFunction, fragment;
      fragment = window.location.hash;
      $li = fragments[fragment];
      if (!$li) return;
      clickFunction = $li.data('clickFunction');
      return clickFunction.apply($li);
    });
    $("#equipe > ul:first, #parceiros-financeiros > ul, #metodologia-cenario > ul").each(function() {
      return createTab($(this));
    });
    $("#principios > ul, #parceiros-divulgacao > ul, #parceiros-tecnicos > ul").each(function() {
      return createTab($(this), false);
    });
    return $(window).trigger('hashchange');
  });

}).call(this);
