dock('#registrationholder', {url:'/inci-site/server/profile'});
dock('#formholder', {url:'/inci-site/server/diva'});
function closebox(){
    (function($){
        $('a.boxclose').click(function(){
            dock('#registrationholder', {url: '/inci-site/server/profile'});
        });
        return false;
    })(jQuery);
}
