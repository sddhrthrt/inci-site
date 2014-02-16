(function($, undefined) {
    
    function resizeCube(w, h, d) {

        function buildWall(el, a, b, rot, move) {
            el.width(a).height(b);
            var prefixes = '-moz- -webkit- -o- '.split(' '),
                axes = 'XYZ', transf = '';

            for (var i=0; i<3; i++) {
              if (rot[i] != 0) {
                 transf += ' rotate' + axes[i] + '( ' + rot[i] + 'deg )';
              }
            }
            for (var i=0; i<3; i++) {
              if (move[i] != 0) {
                 transf += ' translate' + axes[i] + '( ' + move[i] + 'px )';
              }
            }

            for (var i=0, l=prefixes.length; i < l; i++) {
              el.css(prefixes[i] + 'transform', transf);
            }
        }
        buildWall($("#left"), d, h, [0, 90, 0], [d/2, 0, -w/2]);
        buildWall($("#right"), d, h, [0, -90, 0], [-d/2, 0, -w/2]);
        buildWall($("#bottom"), w, d, [90, 0, 0], [0, -d/2, -(h - d/2)]);
        buildWall($("#top"), w, d, [-90, 0, 0], [0, d/2, -d/2]);
        buildWall($("#back"), w, h, [0, 0, 0], [0, 0, -d]);
    }
    function keepIcons(w, h, d){
        var prefixes = '-moz- -webkit- -o- '.split(' '),
            transf = '';
        for(var i=0; i< 4; i++){
            var el = $("#front"+i);
            el.height(h/4).width(w);
            for(var j=0,l=prefixes.length; j<l; j++){
                var dist = ((-d/4)*i-(d/8));
                el.css(prefixes[j] + 'transform', 
                       "translateZ("+dist+"px) translateY(40px)");
            }
            console.log("("+i+") moving "+el.id+" "+((-d/4)*i-(d/8))+"px along z axis");
        }
    }
    $(document).ready(function () {
	function adjust () {
	    var w = $(window).width(),
		h = $(window).height(),
		d = Math.max(h, w);
	    resizeCube(w, h, d);
        keepIcons(w, h, d);
	    return true;
	}
	$(window).resize(adjust);
	adjust();
    });

})(jQuery);
