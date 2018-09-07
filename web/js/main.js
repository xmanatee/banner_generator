
(function ($) {
    "use strict";



  
  
    /*==================================================================
    [ Validate ]*/
    var input = $('.validate-input .input100');

    $('.validate-form').on('submit',function(){
        var check = true;

        for(var i=0; i<input.length; i++) {
            if(validate(input[i]) == false){
                showValidate(input[i]);
                check=false;
            }
        }

        return check;
    });


    $('.validate-form .input100').each(function(){
        $(this).focus(function(){
           hideValidate(this);
        });
    });

    function validate (input) {
        if($(input).attr('type') == 'email' || $(input).attr('name') == 'email') {
            if($(input).val().trim().match(/^([a-zA-Z0-9_\-\.]+)@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.)|(([a-zA-Z0-9\-]+\.)+))([a-zA-Z]{1,5}|[0-9]{1,3})(\]?)$/) == null) {
                return false;
            }
        }
        else {
            if($(input).val().trim() == ''){
                return false;
            }
        }
    }

    function showValidate(input) {
        var thisAlert = $(input).parent();

        $(thisAlert).addClass('alert-validate');
    }

    function hideValidate(input) {
        var thisAlert = $(input).parent();

        $(thisAlert).removeClass('alert-validate');
    }

    function getParam(name) {
        var results = new RegExp('[\?&]' + name + '=([^&#]*)').exec(window.location.href);
        if (results === null){
           return null;
        }
        else{
           return decodeURI(results[1]) || 0;
        }
    }

    $(document).ready(function() {
        // var default_styles = '' +
        //     '.text:after {\n' +
        //     '    content: \'"When I get sad I stop being sad and be AWESOME instead." @Barney Stinson\';\n' +
        //     '}\n\n' +
        //     '#paper:after {\n' +
        //     '    content: "#paper";\n' +
        //     '}\n'
        // ;
        // $("#styles").text(default_styles);
        var img_path_param = getParam("img_path");
        if (img_path_param !== null) {
            // $("#img_div").css("background-image", "url(" + img_path_param + ")");
            $("#img_div").css("background-image", "");
            $("#img").attr("src", img_path_param);
            $("#img_a").attr("href", img_path_param);
            // $("#img_div").click(function() {
            //     location.href=img_path_param;
            // })
            // var iframe = document.getElementById('invisible');
            // iframe.src = img_path_param;
            // $("#img_div").append("<a href='" + img_path_param + "'></a>");
        }
    });


})(jQuery);