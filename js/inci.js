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

(function($){
    $(".cell").mouseenter(
        function(){ 
            var i = $(this).attr("id"); if(i){ $("#"+i+"-lg").addClass('iconbounce'); } 
        }
    );
    $(".cell").mouseleave(
        function(){ 
            var i = $(this).attr("id"); if(i){ $("#"+i+"-lg").removeClass('iconbounce');
            } 
        }
    );        
})(jQuery);
(function($) {
        modals = {
            events: "modals/events.html",
            pronites: "modals/pronites.html",
            beach: "modals/beach.html",
            informalz: "modals/informalz.html",
            icare: "modals/icare.html",
            incispecial: "modals/incispecial.html",
            workshop: "modals/workshops.html",
            sportsfest: "modals/sportsfest.html",
            aboutus: "aboutus.html",
            sponsors: "sponsors.html",
            accomodation: "accomodation.html",
            contactus: "contactus.html",
            registration: "registration.html"
        }
        $('.clickme').bind('click', function(e) {
            e.preventDefault();
            var targetid = e.currentTarget.id.split('-')[0];
            if(! targetid in modals) return;
            console.log("clicked on "+targetid+", opening "+modals[targetid] );
            $("#modal").load(modals[targetid], function(){
                showModal();
            });
            //target.find("iframe").remove();
            //var i = $("<iframe></iframe>").css("width", "100%").css("height", "100%").attr("scrolling", "yes");
            //target.append(i);
            //$('#modal').bPopup({
                //easing: 'easeOutBack', //uses jQuery easing plugin
                //speed: 450,
                //transition: 'slideDown'
            //});
            //var url = modals[targetid];
            //i.attr("src", url);
        });
})(jQuery);
