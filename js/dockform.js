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
            }
        }
        $.ajax(args);
    }
}
