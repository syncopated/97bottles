$(document).ready(function(){
    // Hide and show the "Search..." text in the search box on focus on blur, respectivley.
    $("#search input:eq(0)").bind("blur", function () {
        if($(this).val() === ""){
            $(this).val("Search...");
        }
    }).bind("focus", function(){
        $(this).val('');
    });

    //Moves the footer to the bottom fo the window
    function move_the_footer(){

        //Calculates the difference between the body and the window height
        function calculateDifference() {  
            var brother_height = $(".container:eq(0)").height() + $(".container:eq(1)").height(); 
            return $(window).height() - brother_height - 32;
        }

        $("#footer").css({"marginTop": calculateDifference() + "px" });
        $(window).bind("resize", function(){move_the_footer();});
    }

    // Checks to see if the footer is at the bottom of the window
    // if not it moves it
    if ($("body").height() < $(window).height() - 32) { move_the_footer();}
    $("body").resize(function(){
        move_the_footer();
    });

    /* Add City, Brewery */
    $("#add-city-link").click(function(e){ $("#add-city").slideDown(); e.preventDefault();});
    $("#add-brewery-link").click(function(e){$("#add-brewery").slideDown(); e.preventDefault();});

    /* LightSwitches */
    $(".follow-link").lightSwitch({offText: "follow", onText: "unfollow", ajax_request: true, request_type: "GET", loader: "false"});
    $(".todolist").lightSwitch({offText: "to-drink", onText: "un-to-drink", ajax_request: true, request_type: "POST", loader: "true" });
    $(".add-to-todolist").lightSwitch({offText: "to-drink", onText: "un-to-drink", ajax_request: true, request_type: "POST", loader: "false",
    endofswitch: function(element){
        $(element).parents("tr").remove();} 
    });
    $(".favoriter").lightSwitch({offText: "favorite", onText: "unfavorite", ajax_request: true, request_type: "POST", loader: "true" });
    $(".nasty").lightSwitch({offText: "nasty", onText: "un-nasty", ajax_request: true, request_type: "POST", loader: "true" });
    $(".nothanks").lightSwitch({offText: "no thanks", onText: "un-no-thanks", ajax_request: true, request_type: "POST", loader: 'false', endofswitch: function(element){
        $(element).parents("tr").remove();} 
    });

    $("#id_review-rating").css("visibility", "hidden");

    //Checks to see if the element exists before it loads the datepicker
    if($("#id_profile-birth_date").length > 0){

        $("#id_profile-birth_date").datepicker({
            dateFormat: "yy-mm-dd",
            yearRange: "1940:2009",
            showOn: "focus",
            changeYear: true
        });

    }

    /* recommend slidedown */
    $(".recommend-to-friend").hide();
    $(".recommend").toggle(
        function(e){
            $(".recommend-to-friend").slideDown("fast"); 
            e.preventDefault();
        }, function(e){
            $(".recommend-to-friend").slideUp("fast"); e.preventDefault();
        }); 

        /* Rating Slider */
        $(".slider-bg").show();

        $("#ui-slidey").slider({
            max: 97, 
            min: 0, 
            steps: 97, 
            handle: ".slider", 
            slide: function(e, ui){
                $("#slider-value").text(ui.value);
            }, 
            stop: function(e, ui){ 
                $("#id_review-rating").val(ui.value);
            }, 
            value: $("#id_review-rating").val()
        });
        //If beer is reviewed already, value is set
        if($("#id_review-rating").val() !== ""){
            $("#ui-slidey").slider({ 
                value: $("#id_review-rating").val()
            });         
            $("#slider-value").text($("#id_review-rating").val());
        }


        /* Beer Color Picker */
        $(".beer-color-picker li a").each(function(){
            $(this).click(function(e){
                var color_id = $(this).attr("id") + "";
                $(".beer-color-picker li.selected").removeClass("selected");
                $(this).parent().addClass("selected");
                color_id = color_id.replace(/color=/, "");
                $("#beer-color").val(color_id);
                e.preventDefault();
            });
        });
        
        $(".review-form #delete").click(function(){
            var confirmation = confirm("Are you sure you want to delete your review?");
            if (!confirmation){
                return false;
            } else {
                $(this).submit();
            }
        });
        
        /* Beer, Brewery & City Livesearch */
        $('#beer-search').liveSearch({ajaxURL: '/beer/_search/?search='});
        $('#brewery-search').liveSearch({ajaxURL: '/breweries/_search/?search='});
        $('#city-search').liveSearch({ajaxURL: '/cities/_search/?search='});

        $("#add-city").hide();
        $("#add-brewery").hide();
        $("#openid-homepage").click(function(e){ 
            $("#homepage-sign-in form:eq(0)").hide(); 
            $("#homepage-sign-in form:eq(1)").show();
            e.preventDefault();
        });
        $("#normal-login-homepage").click(function(e){
            $("#homepage-sign-in form:eq(1)").hide(); 
            $("#homepage-sign-in form:eq(0)").show();
            e.preventDefault(); 
        });
        $("#homepage-sign-in form:eq(1)").hide();


});