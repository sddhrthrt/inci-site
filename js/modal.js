window.currentImages = [];

function slideImage(){
    if(window.currentImages){
        (function($){
            var i = parseInt($("#left-modal").attr("seq"));
            if (isNaN(i)){
                $("#left-modal").attr("seq", 0); 
                i = 0;
            } else {
                i = (i + 1) % window.currentImages.length;
                $("#left-modal").attr("seq", i);
            }
            if (window.currentImages.length){
                $("#left-modal").css("background-image", currentImages[i]);
            }
        })(jQuery);
    }
    //try later
    setTimeout(function(){slideImage();}, 5000);
}
slideImage();
function showModal(){
    function adjustModal(){
        function adjustList(sel){
            var lis = $(sel).find("li");
            var len = lis.length;
            $(lis).each(function(){
                $(this).attr("style", "width: "+100/len+"%");
            });
        }
        function adjustListDiv(sel){
            var lis = $(sel).find(".menuitem");
            var len = lis.length;
            $(lis).each(function(){
                $(this).attr("style", "width: "+((100/len)-1)+"%");
            });
            //if( len < 4 ) { $(".menuitem").css("style", "font-size: 18px");};
        }
        adjustList(".menuitems");
        adjustListDiv(".modaltopmenu");
        var lis = $(".menuitems").find("li");
        var len = lis.length;
        $(lis).each(function(){
            $(this).attr("style", "width: "+100/len+"%");
        });
        var modalheight = $("#right-modal").height();
        var topheight = $(".modaltopmenu").height();
        var bottomheight = $(".modalbottommenu").height();
        $("#right-modal div.content").height(modalheight-(topheight+bottomheight)-58);
    }
	$(window).resize(adjustModal);
    adjustModal();
    function showContent(contentbody, sectionid){
        $(contentbody).find("div.section").hide();
        $(contentbody).find("div.section#"+sectionid).show();
    }
    function makeModalMenu(){
        menu = $(".modaltopmenu");
        menu.find(".menuitem").click(function(){
            console.log(this);
            self = $(this);
            self.siblings().removeClass("active");
            self.addClass("active");
            showContent(".content", $(this).attr("id"));
        });
        lid = $(menu.find(".menuitem")[0]).addClass("active").attr("id");
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
    function preregisterbutton(){
        console.log("clicked register");
        button = $(this);
        eventid = button.attr("id").slice(0, -5);
        $.ajax({
            type: "GET",
            url: "/server/preregister/"+eventid,
        }).done(function(response){
            console.log(response['response']);
            switch(response['response']){
                case "login":
                    responsetext = "Please login before registering for this event.";
                    disble = true;
                    break;
                case "success":
                    responsetext = "Successfully registered for this event. ";
                    disable = true;
                    break;
                case "alreadydone":
                    responsetext = "You have already registered for this event. ";
                    disable = true;
                    break;
                case "invalid":
                case "eventnotfound":
                default:
                    responsetext = "Failed, sorry. If you think it's a mistake, mail us.";
                    disable = true;
                    break;
            }
            $(".preregister-reply#"+eventid+"reply").html(responsetext);
            if (disable){
                button.addClass("inactive");
            }

        });
    }
    $.ajax({
        type: "GET",
        url: "/server/idforevent/all"
    }).done(function(response){
        if (response['response'] == 'success'){
            window.idforevents = response['eventids'];
            $.ajax({
                type: "GET",
                url: "/server/ispreregister/all"
            }).done(function(response){
                   console.log("loggedin?: ", response['response']=='success');
                if (response['response'] == 'success'){
                    window.registrations = response['registrations'];
                    window.notloggedin = false;
                } else {
                    window.notloggedin = true;
                }
                $(".section").each(function(){
                    var section = $(this);
                    var sid = $(this).attr('id');
                    eid = window.idforevents[sid];
                    console.log("event: ", sid, "id: ", eid);
                    if (!eid) { return; } //no registration for this event
                    var inactive = false, reply = "";
                    if (window.notloggedin == true){
                        inactive = true;
                        reply = "Log in to register.";
                    } else if (window.registrations[eid]==true){
                        console.log("registered for "+eid)
                        inactive = true;
                        reply = "You have already registered for this event.";
                    } 
                    var preregister = $("<div></div>")
                                     .addClass("preregister")
                                     .append($("<div></div>")
                                             .addClass("preregister-button")
                                             .addClass(inactive?"inactive":"")
                                             .attr("id", ""+eid+"event")
                                             .text("Register")
                                             .bind('click', preregisterbutton))
                                     .append($("<div></div>")
                                             .addClass("preregister-reply")
                                             .attr("id", ""+eid+"reply")
                                             .text(reply));
                    section.prepend(preregister);
                });
                $(".subsection").each(function(){
                    var section = $(this);
                    var sid = $(this).attr('id');
                    eid = window.idforevents[sid];
                    console.log("event: ", sid, "id: ", eid);
                    if (!eid) { return; } //no registration for this event
                    var inactive = false, reply = "";
                    if (window.notloggedin == true){
                        inactive = true;
                        reply = "Log in to register.";
                    } else if (window.registrations[eid]==true){
                        console.log("registered for "+eid)
                        inactive = true;
                        reply = "You have already registered for this event.";
                    } 
                    var preregister = $("<div></div>")
                                     .addClass("preregister")
                                     .append($("<div></div>")
                                             .addClass("preregister-button")
                                             .addClass(inactive?"inactive":"")
                                             .attr("id", ""+eid+"event")
                                             .text("Register")
                                             .bind('click', preregisterbutton))
                                     .append($("<div></div>")
                                             .addClass("preregister-reply")
                                             .attr("id", ""+eid+"reply")
                                             .text(reply));
                    section.prepend(preregister);
                });
            });
        }
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
(function($){
})(jQuery);
