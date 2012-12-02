/* Lightswitch V 1.0.1
Written By: Kenny Meyers
Email: kenny@blueflavor.com
BlueFlavor: http://www.blueflavor.com -- We Build Awesome Websites
----------------------------

The purpose of the lightswitch plug-in: When a user clicks on a 
link, an Ajax request is sent to the anchor tag's url. If a success object (a Json object with success set to true) is returned to the data, the lightswitch will turn off or on depending on its current state

Setup: 

* Select the selector class or id that you would like lightswitch added to. e.g. $("#theSwitch") with the href attribute set to the appropriate request (e.g. <a href="requests/json.jsp"></a>)

2. In the top of your document add the following: 
$("#theSwitch").lightSwitch({
  offText: "Follow",
  onText: "unFollow"
})

3. Make sure your REST architecture returns a simple JSON object back with a property of success set to the string value of "true"

Changelog
=====================

1.1 - Added support for multiple items


*/

;(function($){
  $.fn.lightSwitch = function(options) {

    var opts = $.extend({}, $.fn.lightSwitch.defaults, options || {});
    var o = $.meta ? $.extend({}, opts, $this.data()) : opts;

    return this.each(function(){
      var $this = $(this);

      $this.bind('click', function(e){
        e.preventDefault();
        $.ajax({
          type: o.request_type || "GET",
          url: $this.attr("href"),
          beforeSend: function(){
            if(o.loader === 'true'){
              $this.parent().prepend('<img id="loading-image" src="/static/ninetyseven/assets/img/core/ajax-loader.gif" alt="loading" />');
            };
          },
          contentType: "text/plain",
          data: {},
          dataType: "json",
          error: errorAlert,
          success: function(json){
            if($("#loading-image")){
              $("#loading-image").remove();
            }
            if(json["success"] === 'true'){
                toggleSwitch($this, o);
            }
          }
        });
      });
    });
  }

  $.fn.lightSwitch.defaults = {
    onText: 'On',
    offText: 'Off', 
    ajax_request: true,
    loading: true 
  };

  function toggleSwitch(clicked_item, o) {
    if(clicked_item.text() === o.onText){ 
      clicked_item.text(o.offText);
    } else {
      clicked_item.text(o.onText);
    }
    if(o.endofswitch){
      o.endofswitch(clicked_item);
    }
  };

  function errorAlert(request, textStatus, errorThrown){
    if(console){
      console.log(request + "\nStatus: " + textStatus + "\nError: " + errorThrown);
    }
  };
}) (jQuery);