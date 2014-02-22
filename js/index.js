(function($){
    dock('#registration', {url: 'server/profile'});
    
})(jQuery)
function closebox(){
    (function($){
        $('a.boxclose').click(function(){
            dock('#registration', {url: 'server/profile'});
        });
        return false;
    })(jQuery);
}
