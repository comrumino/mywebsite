var resize_canvas = function(canv, w, h) {
  if (canv != null) {
  canv.width = w;
  canv.height = h;
  canv.style.width = w + 'px';
  canv.style.height = h + 'px';
  }
};

var noise = function(noise_ctx) {
  var w = noise_ctx.canvas.width;
  var h = noise_ctx.canvas.height;
  var idata = noise_ctx.createImageData(w, h);
  var buffer32 = new Uint32Array(idata.data.buffer);
  var len = buffer32.length;
  for (var i=0; i<len; i++) {
    if (!(Math.random() < Math.abs((len/2.0)-i)*Math.sin(i)*2/(len*Math.tan(i))))
      buffer32[i] = 0xff323232;
  }
  noise_ctx.putImageData(idata, 0, 0);
};

var set_canvas_text = function(text_canvas, text_ctx) {
  text_ctx.shadowColor = "#323232"; 
  text_ctx.shadowOffsetY = -5; 
  text_ctx.shadowBlur = 7;
  text_ctx.font = "2.5em Inconsolata";
  let ctx_measure = ctx.measureText(text_ctx);
  let font_sz = (25 * (ctx_measure.actualBoundingBoxDescent + ctx_measure.actualBoundingBoxAscent)) / 10;
  text_ctx.textAlign = "center";
  text_ctx.fillStyle = "#03a9f4";
  text_ctx.fillText("Welcome to stro.nz", Math.floor(text_canvas.width/2), Math.floor(text_canvas.height/2));
  text_ctx.fillText("a Stronz virtual abode", Math.floor(text_canvas.width/2), Math.ceil((text_canvas.height/2)+font_sz));
};

var customRand = function() {
  if (Math.random() > 0.20) 
    return randInt(250,500);
  else 
    return randInt(500,7000);
};

var canvas;
var ctx;
var toggle = true;
var noise_id;
var loop = function() {
  toggle = !toggle;
  if (toggle) {
    noise_id = requestAnimationFrame(loop);
    return;
  } else if (!(window.location.pathname == '/') && !(window.location.pathname == '/home') 
            && !(window.location.pathname == '/home/')) {
    cancelAnimationFrame(noise_id);
    noise_id = undefined;
    console.log('Cancelled animation frame');
    return;
  }
  noise(ctx);
  noise_id = requestAnimationFrame(loop);
};

var overlay;
var octx;
var init = function(noise_canvas, text_canvas) {
  canvas = noise_canvas;
  ctx = canvas.getContext('2d');
  overlay = text_canvas;
  octx = overlay.getContext('2d');

  toggle = true;
  noise_id = requestAnimationFrame(loop);
  set_canvas_text(overlay, octx);
};

var clear = function(tctx) {
  tctx.fillStyle = "rgba(0,0,0,0)";
  tctx.clearRect(0, 0, tctx.width, tctx.height);
  tctx.fill();
};

var landCanvas = function (identity, zIndex) {
    var layer;
    if (document.getElementById(identity) == null) {
        layer = document.createElement('canvas');
        layer.id = identity;
    } else {
        layer = document.getElementById(identity);
    }
    var div = $('#home-content');
    var width = $(div).width();
    var height = window.innerHeight*0.66-55;
    layer.style.zIndex = zIndex;
    layer.style.padding = "10px 0px 0px 0px";
    layer.width = width;
    layer.height = height;
    layer.style.position = "absolute";
    layer.style.top = 0;
    layer.style.left = 0;

    $(div).append(layer); 
    return layer;
};

var resize = function() {
  var width = $('#home-content').width();
  var height = window.innerHeight*0.66-55;
  var snapshot_canvas = landCanvas('snapshot-land-canvas', 0);
  snapshot_ctx = snapshot_canvas.getContext('2d');
  snapshot_ctx.drawImage(canvas, 0, 0);
  resize_canvas(canvas, width, height);
  resize_canvas(overlay, width, height);
  set_canvas_text(overlay, octx);
  ctx.drawImage(snapshot_canvas, 0, 0);
  snapshot_canvas.remove();
};

var randInt = function(a, b) {
  return ~~(Math.random() * (b - a) + a);
};
/* vim:se ts=2 sts=2 sw=2 et: */
