    ////////////////// Função para habiliar o POST
jQuery(document).ajaxSend(function(event, xhr, settings) {
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    function sameOrigin(url) {
        // url could be relative or scheme relative or absolute
        var host = document.location.host; // host + port
        var protocol = document.location.protocol;
        var sr_origin = '//' + host;
        var origin = protocol + sr_origin;
        // Allow absolute or scheme relative URLs to same origin
        return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
            (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
            // or any other URL that isn't scheme relative or absolute i.e relative.
            !(/^(\/\/|http:|https:).*/.test(url));
    }
    function safeMethod(method) {
        return (/^(GET|HEAD|OPTIONS|TRACE)jQuery/.test(method));
    }

    if (!safeMethod(settings.type) && sameOrigin(settings.url)) {
        xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
    }
});
    
    
    var t;
    var timer_is_on=0;
    
    function timedCount()
    {

    
        jQuery.post(
               "/alerts/status/",
               {system: jQuery('#systemid').html(),
                user: jQuery('#userid').html()},
               function(data){
                    if (data != "fail") {
                        jQuery('body').append(data);
                        jQuery('.popup-content').dialog({
                            width:600,
                            close: function() {
                                jQuery(this).remove();
                                },
                            modal:true
                        });
                    }
                    else{
                        //redirects the maluco
                        window.location='/accounts/login/';
                        //alert("faiô!");
                    }
               });
               
        t=setTimeout("timedCount()",30000);
        
    }
    

    function doTimer()
    {
        if (!timer_is_on)
          {
          timer_is_on=1;
          timedCount();
          }
    }

    jQuery(document).ready(function(){
        doTimer();
        });
    
    
