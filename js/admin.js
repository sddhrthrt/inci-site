function setAll (selector, value) {
    $(selector).each(function(){ this.checked = value });
}
$("input[name=eventscheckall]").change(function(){
    setAll(".events input[type='checkbox']", this.checked);
});
$("input[name=participantscheckall]").change(function(){
    console.log(this.checked);
    setAll(".participants input[type='checkbox']", this.checked);
});
$(".events input[type='checkbox']").change(function(){
    var checkedEvents = [];
    $(".events input[type='checkbox']:checked").each(function(){ checkedEvents.push(this.name)});
    $.ajax({
        type: "POST",
        data: JSON.stringify({
            events: checkedEvents,
        }),
        contentType: 'application/json;charset=UTF-8',
        url: '/server/admin/getparticipants',
    }).done(function(response){
        cu = response['checkedusers'];
        setAll(".participants input[type='checkbox']", false);
        for(i=0, l=cu.length; i < l; i++){
            $(".participants input[name='"+cu[i]+"']")[0].checked = true;
        }
    });
});
$("input[name='email'][type='submit']").click(function(){
    var checkedParticipants = [];
    $(".participants input[type='checkbox']:checked").each(function(){ checkedParticipants.push(this.name)});
    $.ajax({
        type: "POST",
        data: JSON.stringify({
            body: $("textarea[name='body']").val(),
            subject: $("textarea[name='subject']").val(),
            to: checkedParticipants,
        }),
        contentType: 'application/json;charset=UTF-8',
        url: '/server/admin/sendemail',
    }).done(function(response){
        console.log(response);
    });
    return false;
});

