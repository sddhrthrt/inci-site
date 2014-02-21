function dock(target, args){
    if (args['url']) {
        args['success'] = function(response){
            if(response.url){
                dock(target, { 
                    url: response.url,
                });
            } else {
                $(target).html(response);
                //contain the submit button and dock the result again.
                $("form").submit(function(event){
                    dock(target, {
                        data: $(this).serialize(),
                        url: $(this).attr('action'),
                        type: $(this).attr('method'),
                    });
                    return false;
                });
                $("a").click(function(event){
                    dock(target, {
                        url: $(this).attr('href'),
                    });
                    return false;
                });
                //special case for multiform
                (function($){
                    $("#divaform").submit(function(event){
                        $(this).ajaxSubmit({
                            target: target,
                            data: $(this).serialize(),
                            url: $(this).attr('action'),
                            type: $(this).attr('method'),
                        });
                        return false;
                    });
                })(jQuery);
            }
        }
        $.ajax(args);
    }
}
