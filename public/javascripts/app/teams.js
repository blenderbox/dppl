var TEAMS = (function($) {
    var app = {}, $el, on = 'on', $scroller = $('#teams-scroller'), cls = '.scrollbar';
    // Public functions
    // app.foo = function() {  };
    // Private functions
    function init() {
        if ($scroller.length < 1) { return; }
        $scroller
            .tinyscrollbar()
            .mouseenter(onScrollerIn)
            .mouseleave(onScrollerOut);
    }
    function onScrollerIn(e){
        $(this)
            .find(cls)
            .addClass(on);
    }
    function onScrollerOut(e){
        $(this)
            .find(cls)
            .removeClass(on);
    }
    $(init);
    return app;
} (jQuery));
