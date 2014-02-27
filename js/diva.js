dock('#registrationholder', {url:'/server/profile'});
dock('#formholder', {url:'/server/diva'});
function closebox(){
    (function($){
        $('a.boxclose').click(function(){
            dock('#registrationholder', {url: '/server/profile'});
        });
        return false;
    })(jQuery);
}
