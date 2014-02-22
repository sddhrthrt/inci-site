function dock(target, args){
    if (args['html']) {
        $(target).html(response);
        //special case for multiform
        (function($){
            $("#divaform").submit(function(event){
                console.log("submiting as divaform");
                $(this).ajaxSubmit({
                    data: $(this).serialize(),
                    url: $(this).attr('action'),
                    type: $(this).attr('method'),
                    success: function(response){
                        dock(target, {
                            html : response,
                        });
                    }
                });
                return false;
            });
        })(jQuery);
    }
    if (args['url']) {
        args['success'] = function(response){
            if(response.url){
                console.log("docking "+response.url+" at "+target);
                dock(target, { 
                    url: response.url,
                });
            } else {
                $(target).html(response);
                //contain the submit button and dock the result again.
                $(target+" form").submit(function(event){
                    if ($(this).id=="#divaform"){
                        console.log("refusing to take on the diva giant");
                        return false;
                    }
                    dock(target, {
                        data: $(this).serialize(),
                        url: $(this).attr('action'),
                        type: $(this).attr('method'),
                    });
                    return false;
                });
                $(target+" a").click(function(event){
                    console.log("docking "+$(this).attr('href')+" at "+target);
                    dock(target, {
                        url: $(this).attr('href'),
                    });
                    return false;
                });
                //special case for multiform
                (function($){
                    $("#divaform").submit(function(event){
                        console.log("submiting as divaform");
                        $(this).ajaxSubmit({
                            data: $(this).serialize(),
                            url: $(this).attr('action'),
                            type: $(this).attr('method'),
                            success: function(response){
                                dock(target, {
                                    html : response,
                                });
                            }
                        });
                        return false;
                    });
                })(jQuery);
            }
        }
        $.ajax(args);
    }
}
