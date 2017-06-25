$(window).on('orientationchange popstate', function(e) {//TODO
    location.reload();
});
$(window).on('resize', function(e) {
    var path = window.location.pathname;
    if (path === '/' || path === '/home/') location.reload();
});


$(document).on('click','.navbar-brand',function(e) {
        if(!$(e.target).siblings(".directoryToggle").hasClass("collapsed")){
            $(this).siblings(".directoryToggle").click();
        }
});

$(document).on('click','.navbar-collapse.in',function(e) {
        if($(e.target).parent().is('.active')){
            e.preventDefault();
        }
    var currentscrollpos;
    if( $(e.target).is('a') && $(e.target).attr('class') != 'dropdown-toggle' ) {
        $(this).collapse('hide');
        currentscrollpos = $(window).scrollTop();
        $("html, body").animate({ scrollTop: currentscrollpos }, 10);
    }
});

$(document).on('click','.directoryToggle',function() {
    var currentscrollpos = $(window).scrollTop();
    $("html, body").animate({ scrollTop: currentscrollpos }, 10);
});

function linkExists(filePath) {
    if (!$("link[href='"+filePath+"']").length){
         var prefetch = document.createElement('link'),
             prerender = document.createElement('link');
         prefetch.rel = 'prefetch';
         prerender.rel = 'prerender';
         prefetch.href = filePath;
         prerender.href = filePath;
         document.head.appendChild(prefetch);
         document.head.appendChild(prerender);
    }
}

$(document).on('click', '.navbar-brand', function (e) {
    if (!$(e.target).siblings(".directoryToggle").hasClass("collapsed")) {
        $(this).siblings(".directoryToggle").click();
    }
});
$(document).on('click', '.navbar-collapse.in', function (e) {
    if ($(e.target).parent().is('.active')) {
        e.preventDefault();
    }
    var currentscrollpos;
    if ($(e.target).is('a') && $(e.target).attr('class') != 'dropdown-toggle') {
        $(this).collapse('hide');
        currentscrollpos = $(window).scrollTop();
        $("html, body").animate({
            scrollTop: currentscrollpos
        }, 10);
    }
});
$(document).on('click', '.directoryToggle', function () {
    var currentscrollpos = $(window).scrollTop();
    $("html, body").animate({
        scrollTop: currentscrollpos
    }, 10);
});

var landCanvas = function (identity) {
    this.canvas = document.createElement('canvas');
    this.canvas.id = identity;
    this.ctx = this.canvas.getContext('2d');
    var div = $('#home-content'),
        divWidth = $(div).width(),
        divHeight = window.innerHeight*0.66-55;
    this.canvas.style.padding = "10px 0px 0px 0px";
    this.canvas.height = divHeight;
    this.canvas.width = divWidth;
    this.canvas.style.position = "absolute";
    this.canvas.style.top = 0;
    this.canvas.style.left = 0;

    $(div).append(this.canvas); 
}
function canvases() {
    $('#home-content').css('position','relative');
    var c0 = landCanvas('land-canvas'), 
        c1 = landCanvas('land-overlay'),
        c2 = landCanvas('land-glitch');
    $.cachedScript("/static/js/noise.js");
}
function pageRefresh() {
    var hash = window.location.hash;
}
function portfolio() {
    $.cachedScript("/static/js/sitemapstyler.js");

    if (window.location.hash)
      loadGist(window.location.hash.substring(1));
}
function handleContent(page) {
    switch (page) {
      case 'home':
        $('#main-content').load('/static/partial/'+page+'.html', canvases);
        break;
      case 'portfolio':
        $('#main-content').load('/static/partial/'+page+'.html', portfolio);
        break;
      default:
        $('#main-content').load('/static/partial/'+page+'.html');
        break;
    }
}

window.onload = function () {
    var path = window.location.pathname;
    if (path === '/' || path === '/home') path = '/home/';
    path = path.slice(1,-1);
    $('#'+path).addClass('active');
    handleContent(path);
}
$('#home,#portfolio,#about-me').each(function (e) {
  $(this).click(function () {
    if (!$(this).hasClass('active')) {
      var path = $(this).attr('id'),
          root = 'static/';
      $(this).addClass('active');
      window.history.pushState(path, "Stronz", "/"+path+"/");
      $('#home.active,#portfolio.active,#about-me.active').not(this).each(function (e) {$(this).removeClass('active');});
      handleContent(path);
    }
  });
});



/**
 * https://api.jquery.com/jquery.getscript/
 **/
jQuery.cachedScript = function( url, options ) {
 
  // Allow user to set any option except for dataType, cache, and url
  options = $.extend( options || {}, {
    dataType: "script",
    cache: true,
    url: url
  });
 
  // Use $.ajax() since it is more flexible than $.getScript
  // Return the jqXHR object so we can chain callbacks
  return jQuery.ajax( options );
};
/**
 * jQuery.browser.mobile (http://detectmobilebrowser.com/)
 **/
(function(a){(jQuery.browser=jQuery.browser||{}).mobile=/(android|bb\d+|meego).+mobile|avantgo|bada\/|blackberry|blazer|compal|elaine|fennec|hiptop|iemobile|ip(hone|od)|iris|kindle|lge |maemo|midp|mmp|mobile.+firefox|netfront|opera m(ob|in)i|palm( os)?|phone|p(ixi|re)\/|plucker|pocket|psp|series(4|6)0|symbian|treo|up\.(browser|link)|vodafone|wap|windows ce|xda|xiino/i.test(a)||/1207|6310|6590|3gso|4thp|50[1-6]i|770s|802s|a wa|abac|ac(er|oo|s\-)|ai(ko|rn)|al(av|ca|co)|amoi|an(ex|ny|yw)|aptu|ar(ch|go)|as(te|us)|attw|au(di|\-m|r |s )|avan|be(ck|ll|nq)|bi(lb|rd)|bl(ac|az)|br(e|v)w|bumb|bw\-(n|u)|c55\/|capi|ccwa|cdm\-|cell|chtm|cldc|cmd\-|co(mp|nd)|craw|da(it|ll|ng)|dbte|dc\-s|devi|dica|dmob|do(c|p)o|ds(12|\-d)|el(49|ai)|em(l2|ul)|er(ic|k0)|esl8|ez([4-7]0|os|wa|ze)|fetc|fly(\-|_)|g1 u|g560|gene|gf\-5|g\-mo|go(\.w|od)|gr(ad|un)|haie|hcit|hd\-(m|p|t)|hei\-|hi(pt|ta)|hp( i|ip)|hs\-c|ht(c(\-| |_|a|g|p|s|t)|tp)|hu(aw|tc)|i\-(20|go|ma)|i230|iac( |\-|\/)|ibro|idea|ig01|ikom|im1k|inno|ipaq|iris|ja(t|v)a|jbro|jemu|jigs|kddi|keji|kgt( |\/)|klon|kpt |kwc\-|kyo(c|k)|le(no|xi)|lg( g|\/(k|l|u)|50|54|\-[a-w])|libw|lynx|m1\-w|m3ga|m50\/|ma(te|ui|xo)|mc(01|21|ca)|m\-cr|me(rc|ri)|mi(o8|oa|ts)|mmef|mo(01|02|bi|de|do|t(\-| |o|v)|zz)|mt(50|p1|v )|mwbp|mywa|n10[0-2]|n20[2-3]|n30(0|2)|n50(0|2|5)|n7(0(0|1)|10)|ne((c|m)\-|on|tf|wf|wg|wt)|nok(6|i)|nzph|o2im|op(ti|wv)|oran|owg1|p800|pan(a|d|t)|pdxg|pg(13|\-([1-8]|c))|phil|pire|pl(ay|uc)|pn\-2|po(ck|rt|se)|prox|psio|pt\-g|qa\-a|qc(07|12|21|32|60|\-[2-7]|i\-)|qtek|r380|r600|raks|rim9|ro(ve|zo)|s55\/|sa(ge|ma|mm|ms|ny|va)|sc(01|h\-|oo|p\-)|sdk\/|se(c(\-|0|1)|47|mc|nd|ri)|sgh\-|shar|sie(\-|m)|sk\-0|sl(45|id)|sm(al|ar|b3|it|t5)|so(ft|ny)|sp(01|h\-|v\-|v )|sy(01|mb)|t2(18|50)|t6(00|10|18)|ta(gt|lk)|tcl\-|tdg\-|tel(i|m)|tim\-|t\-mo|to(pl|sh)|ts(70|m\-|m3|m5)|tx\-9|up(\.b|g1|si)|utst|v400|v750|veri|vi(rg|te)|vk(40|5[0-3]|\-v)|vm40|voda|vulc|vx(52|53|60|61|70|80|81|83|85|98)|w3c(\-| )|webc|whit|wi(g |nc|nw)|wmlb|wonu|x700|yas\-|your|zeto|zte\-/i.test(a.substr(0,4))})(navigator.userAgent||navigator.vendor||window.opera);

if(jQuery.browser.mobile)$.getScript('/static/js/bootstrap.min.js');



function loadGist(hash) {
history.pushState(null, null, '#'+hash);
var codetainer = document.getElementById("codetainer"),
    iFrame = document.createElement("iframe"),
    HTML = '<html><body style="margin:0" onload="parent.resizeIFrame(document.body.scrollHeight)"><script'
         + ' type="text/javascript" src="https://gist.github.com/' + hash + '.js"></script></body></html>';
iFrame.setAttribute("width", "100%");
iFrame.id = "iFrame";
codetainer.innerHTML = "";
codetainer.appendChild(iFrame);

if (iFrame.contentDocument) iFrame.document = iFrame.contentDocument;
else if (iFrame.contentWindow) iFrame.document = iFrame.contentWindow.document;

iFrame.document.open();
iFrame.document.writeln(HTML);
iFrame.document.close();
}

function resizeIFrame(h) {
var iFrame = document.getElementById("iFrame");
iFrame.style.height = parseInt(h) +5+ "px";
}

$(document).on('click', '.portfolio-content', function() {
    loadGist(this.id);
});



