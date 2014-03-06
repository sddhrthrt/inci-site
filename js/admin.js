function setAll (selector, value) {
    $(selector).each(function(){ this.checked = value });
}
function hideUnchecked(selector, value) {
    if (value) {
        $(selector).each(function(){
            if ( ! $(this).find("input")[0].checked ){
                $(this).hide();
            }
        });
    } else {
        $(selector).each(function() {
            $(this).show();
        });
    }
}
var users = [];
var events = [];
var useroptions = {
    keys: ['username', 'email', 'phone'],
};
var eventoptions = {
    keys: ['name', 'details'],
};
(function($){
    $(".userresults").html("loading...");
    $(".eventresults").html("loading...");
    $.ajax({
        type: 'post',
        url: "/server/json/events",
    }).done(function(response){
        $(".userresults").html("Start typing to search Users");
        events = response['events'];
        $.ajax({
            type: 'post',
            url: "/server/json/users",
        }).done(function(response){
            $(".eventresults").html("Start typing to search Events");
            users = response['users'];
            var fu = new Fuse(users, useroptions);
            var fe = new Fuse(events, eventoptions);
            $("input[name='search']").on('keydown', function(){
                $(".userresults").html("").append("<div>Users:</div>").addClass("barhead");
                $(".eventresults").html("").append("<div>Events:</div>").addClass("barhead");
                var text = $(this).val();
                var userresult = fu.search(text);
                for ( i=0,l=userresult.length; i<l; i++) {
                    $('.userresults').append(
                        $("<div></div>").addClass("resultitem entry user").attr("id", userresult[i]['id'])
                                        .append( $("<div></div>").addClass("username").text(userresult[i]['username']))
                                        .append( $("<div></div>").addClass("userdetails").text(userresult[i]['email']+" - "+userresult[i]['phone']))
                    );
                }
                var eventresult = fe.search(text);
                for ( i=0,l=eventresult.length; i<l; i++) {
                    $('.eventresults').append(
                        $("<div></div>").addClass("resultitem entry event").attr("id", eventresult[i]['id'])
                                        .append( $("<div></div>").addClass("eventname").text(eventresult[i]['name']))
                                        .append( $("<div></div>").addClass("eventdetails").text(eventresult[i]['details']))
                    );
                }
                function formatKeyValue(key, value){
                    return "<span class='key'>"+key+"</span><span class='value'>"+value+"</span>";
                }
                function makeEntry(entry){
                    return "<div class='entry'>"+entry+"</div>";
                }
                function showEvents(registered){
                    var col = $("<div></div>").addClass("entry");
                    for ( var i=0, l=events.length; i<l; i++){
                        var trueorfalse = _.contains(registered, events[i]['id']);
                        
                        var entry = "<span class='key'>"+events[i]['name'];
                        var checked = "";
                        if ( trueorfalse ) checked="checked='checked'";
                        entry += "<input type='checkbox' class='registerfor'"+checked+" name='"+events[i]['id']+"' id='"+events[i]['id']+"' />";
                        entry+="</span><span class='value'>"+events[i]['details']+"</span>";

                        var entrydiv = $("<div></div>").addClass("entry").html(entry);
                        entrydiv.addClass(trueorfalse?"true":"false");
                        col.append(entrydiv);
                    }
                    return col;
                }

                $(".userresults .entry").click(function(){
                    $(".details").html("loading...");
                    var self = $(this);
                    $.ajax({
                        type: 'post',
                        url: "/server/json/user/"+self.attr("id"),
                    }).done(function(response){
                        $(".details").html("").append($("<div>Details:</div>").addClass("barhead"));
                        var profile = $("<div></div>").addClass("userprofile entry").attr("id", response['id']);
                        var keys = ["name", "username", "email", "phone", "college", "fb_username"];
                        for ( i = 0, l = keys.length; i < l; i++){
                            profile.append($(makeEntry(formatKeyValue(keys[i], response[keys[i]]))));            
                        }
                        $(".details").append(profile);
                        $(".details").append($("<div>Registrations (green are registered):</div>").addClass("barhead"));
                        $(".details").append(showEvents(response['registrations']));
                        $(".registerfor").change(function() { 
                            var checkbx = this;
                            $.ajax({
                                type: 'post',
                                url: '/server/adminpreregister',
                                data: JSON.stringify({
                                    eventid: this.id,
                                    userid: $(".userprofile").attr("id"),
                                    state: this.checked
                                }),
                                contentType: 'application/json;charset=UTF-8',
                            }).done(function(response){
                                console.log(response['response']);
                                if(checkbx.checked){
                                    if(response['response']=='successfullyadded'){
                                        $($(checkbx).parents('.entry')[0]).removeClass('false').addClass('true');
                                    } else {
                                        checkbx.checked = false;
                                    }
                                } else {
                                    if(response['response']=='successfullyremoved'){
                                        $($(checkbx).parents('.entry')[0]).removeClass('true').addClass('false');
                                    } else {
                                        checkbx.checked = true;
                                    }
                                }

                            });
                        });
                    });
                });
                $(".eventresults .entry").click(function(){
                    $(".details").html("loading...");
                    var self = $(this);
                    $.ajax({
                        type: 'post',
                        url: "/server/json/event/"+self.attr("id"),
                    }).done(function(response){
                        $(".details").html("").append($("<div>Registrants:</div>").addClass("barhead"));
                        _.each(_.filter(users, function(u){return _.contains(response['registrations'], u['id'] )}), function(user){
                            $('.details').append(
                                $("<div></div>").addClass("resultitem entry user").attr("id", user['id'])
                                                .append( $("<div></div>").addClass("username").text(user['username']))
                                                .append( $("<div></div>").addClass("userdetails").text(user['email']+" - "+user['phone']))
                            );
                        });
                    });
                });
            });
        });
    });
})(jQuery);

(function($){
    dock('#addparticipantform', {url: '/server/addparticipant'});
})(jQuery)


