(function($){
})(jQuery);
function slideImage(images){
    (function($){
        var i = parseInt($("#left-modal").attr("seq"));
        if (isNaN(i)){
            $("#left-modal").attr("seq", 0); 
            i = 0;
        } else {
            i = (i + 1) % images.length;
            $("#left-modal").attr("seq", i);
        }
        $("#left-modal").css("background-image", images[i]);
    })(jQuery);
}
function showModal(){
    function adjustModal(){
        function adjustList(sel){
            var lis = $(sel).find("li");
            var len = lis.length;
            $(lis).each(function(){
                $(this).attr("style", "width: "+100/len+"%");
            });
        }
        adjustList(".menuitems");
        adjustList(".modaltopmenu ul");
        console.log("height: "+$(".modaltopmenu").clientHeight);
        var lis = $(".menuitems").find("li");
        var len = lis.length;
        $(lis).each(function(){
            $(this).attr("style", "width: "+100/len+"%");
        });
        var modalheight = $("#right-modal").height();
        var topheight = $(".modaltopmenu").height();
        var bottomheight = $(".modalbottommenu").height();
        $("#right-modal div.content").height(modalheight-(topheight+bottomheight)-10-16);
    }
	$(window).resize(adjustModal);
    adjustModal();
    function showContent(contentbody, sectionid){
        $(contentbody).find("div.section").hide();
        $(contentbody).find("div.section#"+sectionid).show();
    }
    function makeModalMenu(){
        menu = $(".modaltopmenu");
        menu.find("li").click(function(){
            console.log(this);
            self = $(this);
            self.siblings().removeClass("active");
            self.addClass("active");
            showContent(".content", $(this).attr("id"));
        });
        lid = $(menu.find("li")[0]).addClass("active").attr("id");
        showContent(".content", lid);
    }
    makeModalMenu();
    function slideModalIn(){
        $("#modal-frame").addClass("slideDown");
        setTimeout(function(){$("#left-modal").addClass("leftSlideLeft");}, 1000);
    }
    //setTimeout(showModal, 1000);
    $("#modal-darkbg").click(function(){
        hideModal();
    });
    console.log("The modal open now is: ", $("#modal-overlay"));
    $("#modal-overlay").animate({
        opacity: 1,
    }, 200, function(){
        slideModalIn();
    });
}
function hideModal(){
    function slideModalOut(){
        $("#left-modal").addClass("leftSlideRight");    
        setTimeout(function(){$("#modal-frame").addClass("slideOutUp");}, 800);
        setTimeout(function(){
            $("#modal-overlay").animate(
                { opacity: 0, }
            )}, 
            1200);
        setTimeout(function(){$("#modal").children("div").remove();}, 1000);
    }
    slideModalOut();
}
