var canvas = document.getElementById('land-canvas'),
    ctx = canvas.getContext('2d');
canvas.style.zIndex=0;
var overlay = document.getElementById('land-overlay'),
    octx = overlay.getContext('2d');
overlay.style.zIndex=1;
var goverlay = document.getElementById('land-glitch'),
    goctx = goverlay.getContext('2d');
goverlay.style.zIndex=2;

function resize(canv,w,h) {
    canv.width = w;
    canv.height = h;
    canv.style.width = w + 'px';
    canv.style.height = h + 'px';
}

function wrap() {
   var div = $('#home-content'),
        divWidth = $(div).width(),
        divHeight = window.innerHeight*0.66-55;
    resize(canvas,divWidth,divHeight);
    resize(overlay,divWidth,divHeight);
}
wrap();
window.onresize = wrap;

function noise(ctx) {

    var w = ctx.canvas.width,
        h = ctx.canvas.height,
        idata = ctx.createImageData(w, h),
        buffer32 = new Uint32Array(idata.data.buffer),
        len = buffer32.length,
        i = 0;

    for(; i < len;i++) {
        if (!(Math.random() < Math.abs((len/2.0)-i)*Math.sin(i)*2/(len*Math.tan(i)))) {
        buffer32[i] = 0xff323232;
        }
    }
    ctx.putImageData(idata, 0, 0);
}
var toggle = true;
// added toggle to get 30 FPS instead of 60 FPS
(function loop() {
    toggle = !toggle;
    if (toggle) {
      requestAnimationFrame(loop);
      return;
    } else if (!(window.location.pathname == '/') && !(window.location.pathname == '/home') 
            && !(window.location.pathname == '/home/')) {
      console.log('Dirty throw to break loop, will cleanup later');
      throw '';
    }
    noise(ctx);
    requestAnimationFrame(loop);
})();

var img = new Image()
  , w
  , h
  , offset
  , glitchInterval
  , dataURL;
octx.shadowColor = "#323232"; 
octx.shadowOffsetY = -5; 
octx.shadowBlur = 7;
octx.font = "2.5em Inconsolata";
octx.textAlign = "center";
octx.fillStyle= "#03a9f4";
octx.fillText("Welcome to stro.nz, a Stronz virtual abode",canvas.width/2,canvas.height/2);
dataURL = overlay.toDataURL('image/png',1);
//octx.fillStyle = "rgba(0,0,0,0)";
//octx.clearRect(0, 0, canvas.width, canvas.height);
//img.src = "assets/Hello-World.png";
img.src=dataURL;
img.onload = function() {
  init();
  window.onresize = init;
};

function customRand() {
if (Math.random() > 0.20) {
    return randInt(250,500);
} else {
    return randInt(500,7000);
}
}
var init = function() {
        reset();
        clearInterval(glitchInterval);
        w = overlay.width;
        h = overlay.height;
        /*glitchInterval = setInterval(function() {
                reset();
                setTimeout(glitchImg, randInt(750,2000));
                reset();
        }, customRand());*/
};
var clear = function(tctx) {
    tctx.fillStyle = "rgba(0,0,0,0)";
    tctx.clearRect(0, 0, w, h);
    tctx.fill();
};
var reset = function() {
    clear(octx);
    octx.drawImage(img, 0, 0);
    clear(goctx);
};

var glitchImg = function() {
        for (var i = 0; i < randInt(1,11); i++) {
                var x = randInt(w/6,w);
                var y = randInt(4*h/9,5*h/9);
                var spliceWidth = randInt(-w/250,w/250);
                var spliceHeight = randInt(0,h/30);
                goctx.drawImage(overlay, 0, y, spliceWidth, spliceHeight, x, y, spliceWidth, spliceHeight);
                goctx.drawImage(overlay, spliceWidth, y, x, spliceHeight, 0, y, x, spliceHeight);
                if (Math.random()>0.33)
                  octx.clearRect(0, y, spliceWidth, spliceHeight);
                if (Math.random()>0.33)
                  octx.clearRect(spliceWidth, y, x, spliceHeight);

        }
};

var randInt = function(a, b) {
        return ~~(Math.random() * (b - a) + a);
};

