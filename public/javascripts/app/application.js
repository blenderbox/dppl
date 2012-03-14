// usage: log('inside coolFunc', this, arguments);
window.log = function f(){ log.history = log.history || []; log.history.push(arguments); if(this.console) { var args = arguments, newarr; args.callee = args.callee.caller; newarr = [].slice.call(args); if (typeof console.log === 'object') log.apply.call(console.log, console, newarr); else console.log.apply(console, newarr);}};

(function(a){function b(){}for(var c="assert,count,debug,dir,dirxml,error,exception,group,groupCollapsed,groupEnd,info,log,markTimeline,profile,profileEnd,time,timeEnd,trace,warn".split(","),d;!!(d=c.pop());){a[d]=a[d]||b;}})
(function(){try{console.log();return window.console;}catch(a){return (window.console={});}}());

var APP = (function($) {
    var app = {}, $el, $signIn = $('#sign-in form'), $flag = $('#sign-in .flag'), on = 'on';
    // Public functions
    app.rotate = function(el, tarR) {
        var roto = 'rotate(' + tarR + 'deg)';
        el.style.WebkitTransform = roto;
        el.style.MozTransform = roto;
        el.style.OTransform = roto;
        el.style.MSTransform = roto;
    };
    // Private functions
    function init() {
        $('a[href=#]').attr('href', 'javascript:;');
        // Open links starting with "http(s)://" in a new window unless they're targeted at this host.
        $("a[href^=http]").click(open);
        // Set up the global ajax
        $.ajaxSetup({ cache: false, error: function errorLog(x, e) { log(x, e); }, type: 'POST' });
        if (!Modernizr.input.placeholder) { placeholder(); }
        yepnope([{
            test:Modernizr.csstransitions,
            nope:STATIC_URL + 'javascripts/app/css3.js'
        }]);
        $('#sign-in')
            .find('a')
              .click(toggleSignInForm)
              .mouseenter(onSignInOver)
              .mouseleave(onSignOut)
            .end()
            .find('form')
              .submit(login);
        $('a.more')
            .mouseenter(onMoreOver)
            .mouseleave(onMouseOut);
        $('.bar').each(function(idx, el){
            $el = $(el);
            $el.delay(150).width(($el.data('percent') / 100) * 170);
        });
        emails();
        $('a[rel="tooltip"]').twipsy({ html:true });
        $('.pie').each(calculatePie);
        var kkeys = [],
            konami = "38,38,40,40,37,39,37,39,66,65,13";
        $(document).keydown(function(e) {
          kkeys.push(e.keyCode);
          if (kkeys.toString().indexOf(konami) >= 0) {
            kkeys = [];
            $("body").addClass("tyte");
          }
        });
    }
    function calculatePie(idx, el) {
        $el = $(el);
        app.rotate($el.find('ul :nth-child(4) p')[0], ($el.data('points') - 2) * 90);
    }
    function emails() {
        $el = $('span.e');
        var e = $el.text().split('//').join('.').split('/').join('@');
        $el.after('<a href="mailto:' + e + '">' + e + '</a>');
        $el.remove();
    }
    function login(e) {
      e.preventDefault();
      var $el = $(e.target),
          $error_message = $el.find('p'),
          $sign_in = $("#sign-in"),
          original_height = $sign_in.height();
      $.post($el.attr('action'), $el.serialize(), function(data) {
        if (data.success) {
          $("#sign-in").slideUp(250, function() {
            $("#logged-in-template").tmpl(data.user).insertAfter("header:first");
          });
        } else {
          $error_message.text(data.message).addClass(on);
          if (!$sign_in.hasClass('embiggened')) {
            $sign_in.css({ height: "+=" + $error_message.outerHeight() })
              .addClass('embiggened');
          }
        }
      }, "json");
    }
    function open(e) {
        e.preventDefault();
        var href = this.getAttribute("href");
        if (window.location.host !== href.split('/')[2]) {
            window.open(href);
        } else {
            window.location = href;
        }
    }
    function placeholder() {
        var attr = 'placeholder';
        $('input[' + attr + '!=""]').each(function(idx, el){
            $el = $(el);
            var d = $el.attr(attr);
            if (d === undefined) { return; }
            $el.focus(function onFocus() {
                if (this.value === d) { this.value = ''; }
            }).blur(function onBlur() {
                if ($.trim(this.value) === '') { this.value = d; }
            });
            $el.blur();
        });
    }
    function toggleSignInForm(e) {
        e.stopPropagation();
        if ($signIn.hasClass(on)) {
          $signIn.removeClass(on);
        } else {
          $signIn.find('input:first').focus();
          $signIn.addClass(on);
        }
    }
    function onMoreOver(e) { $(e.currentTarget).parent().addClass(on); }
    function onMouseOut(e) { $(e.currentTarget).parent().removeClass(on); }
    function onSignInOver(e) { $flag.addClass(on); }
    function onSignOut(e) { $flag.removeClass(on); }
    
    // Call the init function on load
    $(init);
    return app;
} (jQuery));
