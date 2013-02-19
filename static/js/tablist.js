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
      $el_li = $el.find('> li');
      li_width = $el.parent().width() / $el_li.length;
      el_minHeight = 0;
      $el_li.each(function(index) {
        var $li, $this, $title;
        $this = $(this);
        $title = $this.find('blockquote > h1').remove();
        $li = $('<li>').append($title.contents());
        $ul.append($li.css({
          width: li_width
        }));
        $li.data('content', $this);
        $li.click(onItemClick);
        $this.hide();
        if (index === 0) return $li.click();
      });
      return $el.before($ul);
    };
    return $('#equipe > ul:first , #principios > ul,\n#parceiros-financeiros > ul, #parceiros-divulgacao > ul, #parceiros-tecnicos > ul,\n#metodologia-cenario > ul').each(function() {
      return createTab($(this));
    });
  });

}).call(this);
