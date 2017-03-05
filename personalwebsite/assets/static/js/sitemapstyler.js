// global namespace
var dtStyler = dtStyler || {};

// declare constants
dtStyler.active_color = "#03a9f4";
dtStyler.inactive_color = "#ffffff";
dtStyler.target_class = "dtStlyer";

// declare objects
dtStyler.History = function() {
  // responsible for tracking previous related clicks
  this.level = [];
  this.loaded = null;

  this.spliceEnd = function(pair) {
    var start = pair.level,
      poppedPair;
    while (start <= this.level.length) {
      poppedPair = this.level.pop();
      if (poppedPair != pair)
        poppedPair.toggleDisplay();
    }
    if (poppedPair != pair)
      this.level.push(pair);
  };

  this.update = function(e, target) {
    e.preventDefault();
    if (!$(this).hasClass("active")) {
      $(target).addClass('active');
      $(this.loaded).removeClass('active');
      this.loaded = $(target);
    }
  };
};

dtStyler.PlusMinus = function() {
  // defines the plus and minus icons
  this.px = 13;
  this.w = this.h = this.px * 0.45;
  this.dx = this.dy = this.px * 0.55;
  this.plus = [
    [0, 0, this.w, this.h],
    [this.dx, 0, this.w, this.h],
    [0, this.dy, this.w, this.h],
    [this.dx, this.dy, this.w, this.h]
  ];
  this.minus = [
    [0, 0, this.px, this.h],
    [0, this.dy, this.px, this.h]
  ];
  // create canvas object
  this.canvas = document.createElement('canvas');
  this.ctx = this.canvas.getContext("2d");
  this.ctx.canvas.width = this.ctx.canvas.height = this.px;
  this.ctx.fillStyle = dtStyler.inactive_color;
  this.canvas.className = "collapsed";

  this.drawIcon = function() {
    var icon = ($(this.canvas).hasClass("collapsed")) ? "plus" : "minus";
    this.ctx.clearRect(0, 0, this.px, this.px);
    if (icon == "plus") {
      for (var i = 0; i < this.plus.length; i++)
        this.ctx.fillRect(this.plus[i][0], this.plus[i][1], this.plus[i][2], this.plus[i][3]);
    } else if (icon == "minus") {
      for (var i = 0; i < this.minus.length; i++)
        this.ctx.fillRect(this.minus[i][0], this.minus[i][1], this.minus[i][2], this.minus[i][3]);
    }
  };

  this.setCanvasColor = function(colour) {
    this.ctx.fillStyle = colour;
    this.drawIcon();
    console.log('canvas ' + this.id + ' fillStlye set to ' + colour);
  };
};

dtStyler.Pair = function(a, ul) {
  // pairs related sibling tags
  this.a = a;
  this.ul = ul;
  this.level = $(this.a).parentsUntil('#sitemap', 'ul').length;
  this.selector = [this.a];

  this.isActive = function() {
    return $(this.a).hasClass('active'); //return (this.a.classList.contains('active'));
  };

  this.toggleActive = function() {
    if (this.isActive()) {
      $(this.a).removeClass('active'); //this.a.classList.remove('active');
    } else {
      $(this.a).addClass('active');
    }
  };
};

dtStyler.PairCanvas = function(a, ul) {
  // call the base constuctors, encapsulates canvas and pair
  dtStyler.PlusMinus.call(this);
  dtStyler.Pair.call(this, a, ul);
  this.selector.push(this.canvas);
  this.drawIcon();

  this.toggleActive = function() {
    if (this.isActive()) {
      $(this.a).removeClass('active'); //this.a.classList.remove('active');
      $(this.canvas).removeClass('active');
    } else {
      $(this.a).addClass('active');
      $(this.canvas).addClass('active');
    }
  };

  this.toggleDisplay = function() {
    if (this.ul) {
      if ($(this.ul).hasClass("expanded")) {
        $(this.ul).addClass("collapsed").removeClass("expanded").slideUp("slow");
        $(this.canvas).addClass("collapsed").removeClass("expanded");
      } else {
        $(this.ul).addClass("expanded").removeClass("collapsed").slideDown("slow");
        $(this.canvas).addClass("expanded").removeClass("collapsed");
      }
    }
    this.drawIcon();
  };
  console.log('paired canvas ' + this.id + ' with a tag');
};

dtStyler.updatePadding = function() {
  // calculates rhs padding so that entire rectangle is clickable
  var listem = $('#dtStyler').find('a:visible'),
    largest = 0;
  for (var i = listem.length - 1; 0 <= i; i--) {
    largest = (largest >= parseInt(listem.eq(i).css('padding-left'), 10) + listem.eq(i).width()) ? largest : parseInt(listem.eq(i).css('padding-left'), 10) + listem.eq(i).width();
  }
  largest = largest + 5;
  for (var i = listem.length - 1; 0 <= i; i--) {
    var fill = largest - parseInt(listem.eq(i).css('padding-left'), 10) - listem.eq(i).width();
    listem.eq(i).css({
      'paddingRight': fill + 'px'
    });
  }
  //$('#codetainer').css({'paddingLeft':$('#dtStyler').width()});
};

dtStyler.pairSync = function(pair) {
  // sync all aspsects pairs
  pair.toggleDisplay();
  dtStyler.history.spliceEnd(pair);
  //dtStyler.updatePadding();// uncomment line for dynamic width
};

dtStyler.colorSync = function(pair) {
  // sync canvas and a-tag colors
  pair.toggleActive();
  if ($(pair.a).hasClass('active') || $(pair.canvas).hasClass('active'))
    pair.setCanvasColor(dtStyler.active_color);
  else
    pair.setCanvasColor(dtStyler.inactive_color);

  console.log('colorSync active.');
};

dtStyler.sync = function(node) {
  // sync all relevant aspects of the node
  var li = node,
    a = node.getElementsByTagName("a")[0],
    ul = node.getElementsByTagName("ul")[0],
    pair;
  if (li.getElementsByTagName("ul").length > 0) {
    ul.style.display = "none";
    ul.className = "collapsed";
    pair = new dtStyler.PairCanvas(a, ul);
    $(pair.selector).on('click', dtStyler.pairSync.bind(this, pair));
    $(pair.selector).on('mouseenter mouseleave', dtStyler.colorSync.bind(this, pair));
    li.appendChild(pair.canvas);
  } else {
    pair = new dtStyler.Pair(a, ul);
    $(pair.selector).on('click', function(e) {
      dtStyler.history.update(e, this);
    });
  }
};

dtStyler.generateIcons = function(dt) {
  // append icons/canvases to li
  var nodes = dt.getElementsByTagName("li"),
    node;
  dtStyler.updatePadding();
  for (var i = 0; i < nodes.length; i++) {
    node = nodes[i];
    dtStyler.sync(node);
  }
};

dtStyler.directorytreeStyler = function() {
  var dt = document.getElementById("dtStyler");
  if (dt)
    dtStyler.generateIcons(dt);
};

// Main
$(document).ready(function() {
dtStyler.history = new dtStyler.History();
dtStyler.directorytreeStyler();
  var git_hash = window.location.hash;
  if (git_hash) {
    $(git_hash).addClass('active');
    loadGist(git_hash.substring(1));
    dtStyler.history.loaded = $(git_hash);
  }
$('#portfolio-content').css("visibility", "visible");
});
