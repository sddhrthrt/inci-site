(function($){
    function adjustList(sel){
        var lis = $(sel).find("li");
        var len = lis.length;
        $(lis).each(function(){
            $(this).attr("style", "width: "+100/len+"%");
        });
    }
    adjustList(".menuitems");
    adjustList(".modaltopmenu ul");
    var lis = $(".menuitems").find("li");
    var len = lis.length;
    $(lis).each(function(){
        $(this).attr("style", "width: "+100/len+"%");
    });
    var modalheight = $("#right-modal").height();
    var topheight = $(".modaltopmenu").height();
    var bottomheight = $(".modalbottommenu").height();
    $("#right-modal div.content").height(modalheight-(topheight+bottomheight)-10-16);
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
    function showModal(){

    }
})(jQuery);
function slideImage(images){
    (function($){
        var i = parseInt($("#left-modal").attr("seq"));
        console.log("got "+i);
        if (isNaN(i)){
            $("#left-modal").attr("seq", 0); 
            i = 0;
        } else {
            i = (i + 1) % images.length;
            $("#left-modal").attr("seq", i);
        }
        console.log("setting "+i+" ("+images[i]+")");
        $("#left-modal").css("background-image", images[i]);
    })(jQuery);
}