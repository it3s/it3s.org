(function() {

  $(function() {
    var createTab, onItemClick;
    onItemClick = function(evt) {
      var $content, $this;
      $this = $(this);
      $this.parent().find('.active').removeClass('active');
      $this.addClass('active');
      $content = $this.data('content');
      $content.parent().find('> li').hide();
      return $content.show();
    };
    createTab = function($el) {
      var $el_li, $ul, el_minHeight, li_width;
      $el.addClass('tablist-content');
      $ul = $('<ul>').addClass('tablist');
      $el_li = $el.find('li');
      li_width = $el.parent().width() / $el_li.length;
      el_minHeight = 0;
      $el_li.each(function(index) {
        var $li, $this, this_height;
        $this = $(this);
        $li = $('<li>').append($this.find('blockquote > h1').contents());
        $ul.append($li.css({
          width: li_width
        }));
        $li.data('content', $this);
        $li.click(onItemClick);
        el_minHeight = parseInt($el.css('min-height'), 10) || 0;
        this_height = $this.height();
        $el.css('min-height', (el_minHeight > this_height ? el_minHeight : this_height));
        $this.hide();
        if (index === 0) return $li.click();
      });
      $el.css('min-height', el_minHeight + 35);
      return $el.before($ul);
    };
    return $('#equipe > ul, #principios > ul').each(function() {
      return createTab($(this));
    });
  });

}).call(this);
