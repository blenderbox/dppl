var TEAMS = (function($) {
    var app = {}, $el, on = 'on';
    // Public functions
    // app.foo = function() {  };
    // Private functions
    function init() {
        $('#teams-scroller').tinyscrollbar();
        $('#teams-scroller').mouseenter(onScrollerIn).mouseleave(onScrollerOut);
    }
    function onScrollerIn(e){
        $(this).find('.scrollbar').addClass(on);
    }
    function onScrollerOut(e){
        $(this).find('.scrollbar').removeClass(on);
    }
    $(init);
    return app;
} (jQuery));
