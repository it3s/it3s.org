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
      var $el_li, $ul, li_width;
      $el.addClass('tablist-content');
      $ul = $('<ul>').addClass('tablist');
      $el_li = $el.find('li');
      li_width = $el.parent().width() / $el_li.length;
      $el_li.each(function() {
        var $li, $this;
        $this = $(this);
        $this.hide();
        $li = $('<li>').append($this.find('blockquote > h1').contents());
        $ul.append($li.css({
          width: li_width
        }));
        $li.data('content', $this);
        return $li.click(onItemClick);
      });
      return $el.before($ul);
    };
    return $('#equipe > ul, #principios > ul').each(function() {
      return createTab($(this));
    });
  });

}).call(this);
