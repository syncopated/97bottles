//these functions complements of 
//http://www.openjs.com/scripts/dom/class_manipulation.php
function get_obj(ele_id){
  return document.getElementById(ele_id);
}
function hasClass(ele,cls) {
  return ele.className.match(new RegExp('(\\s|^)'+cls+'(\\s|$)'));
}
function addClass(ele,cls) {
  if (!this.hasClass(ele,cls)) ele.className += " "+cls;
}
function removeClass(ele,cls) {
  if (hasClass(ele,cls)) {
    var reg = new RegExp('(\\s|^)'+cls+'(\\s|$)');
    ele.className=ele.className.replace(reg,' ');
  }
}

function get_review_count(){
  var elements = document.getElementsByTagName("em");
  for(var i = 0; i < elements.length; i++){
    if(elements[i].parentNode.id === "reviews-link"){
      var review_count = elements[i].childNodes[0].nodeValue; 
      review_count = review_count.replace("(", "");
      review_count = review_count.replace(")", "");
      review_count = review_count * 1; 
      return review_count;
    }
  }
  
}

function load_req(e, req_method, gen_func){
  e.preventDefault();
  var url = get_url(e);
  var req = new XMLHttpRequest();
  req.onreadystatechange = function(){gen_func(e, req);};
  req.open(req_method, url, true);
  req.setRequestHeader("X-Requested-With", "XMLHttpRequest");
  req.send(" ");
}

function process_reviews_req(e, req){
  if (req.readyState === 1){
    var ldng = create_loading_image();
    var content = get_obj("content");
    content.appendChild(ldng, get_obj("header"));
  }
  if (req.readyState === 4 && req.status === 200){
    var content = get_obj("content");
    content.removeChild(get_obj("loading"));
    var html = req.responseText;
    document.getElementById("listing").innerHTML += html;
    change_url(document.getElementById("get-more-reviews"));
    var total_review_count = get_review_count();
    var review_count = document.getElementsByClassName("rating").length - 1;
    if(review_count >= total_review_count ){
      var review_container = get_obj("reviews");
      review_container.childNodes[3].innerHTML = "";
    }
  }
}

//TODO Find a better way to deal with this
function process_favorites_req(e, req){
  if (req.readyState === 1){
    var ldng = create_loading_image();
    var content = get_obj("content");
    content.appendChild(ldng);
  }
  if (req.readyState === 4 && req.status === 200){
    var content = get_obj("content");
    content.removeChild(get_obj("loading"));
    var targeted_element = e.target;
    var favoriter_node = targeted_element.childNodes;
    var favoriter_text = favoriter_node[0].nodeValue;
    if(favoriter_text === "favorite") {
      favoriter_node[0].nodeValue  = "unfavorite";
    } else if (favoriter_text === "unfavorite") {
      favoriter_node[0].nodeValue = "favorite";
    }
    
    if(favoriter_text === "nasty") {
      favoriter_node[0].nodeValue  = "un-nasty";
    } else if (favoriter_text === "un-nasty") {
      favoriter_node[0].nodeValue = "nasty";
    }
    
    if(favoriter_text === "to-drink") {
      favoriter_node[0].nodeValue  = "un-to-drink";
    } else if (favoriter_text === "un-to-drink") {
      favoriter_node[0].nodeValue = "to-drink";
    }
  }
}  

function process_city_req(e, req){
  if(req.readyState === 1){
    var ldng = create_loading_image();
    var content = get_obj("content");
    content.appendChild(ldng); 
  }
  if(req.readyState === 4 && req.status === 200){
    var content = get_obj("content");
    content.removeChild(get_obj("loading"));
    content.appendChild(create_city_div(req.responseText));
    var city_box_close = get_obj("close-city-box");
    city_box_close.addEventListener("click", function(e){
       e.preventDefault();
       var content = get_obj("content");
       content.removeChild(get_obj("city-box"));
   }, false);
   var list = document.getElementsByClassName("add-city-to-form");
   for(var i = 0; i < list.length; i++){
     list[i].addEventListener("click", function(e){
        var cityform = get_obj("id_review-city");
        var content = get_obj("content");
        var cityinput = get_obj("city-search-form");
        cityinput.value = "";
        cityform.value = e.target.id;
        cityinput.value = e.target.childNodes[0].nodeValue;
        content.removeChild(get_obj("city-box"));
        e.preventDefault();
      }, false);
    };
  }
}

function create_city_div(html){
  var loading_div = document.createElement("div");
  loading_div.innerHTML = html;
  loading_div.id = "city-box";
  var new_position = get_center_position({"height": 270, "width": 220});
  loading_div.style.position = "absolute";
  loading_div.style.zIndex = 2001;
  loading_div.style.top = new_position["margin-top"];
  loading_div.style.left = new_position["margin-left"];
  return loading_div;
}

function create_loading_image(){
  var loading_img = document.createElement("img");
  var loading_div = document.createElement("div");
  loading_img.src = "/static/ninetyseven/assets/mobile/siteimages/loading.gif";
  loading_img.title = "Loading...";
  loading_img.alt = "Loading";
  loading_div.id = "loading";
  loading_img.setAttribute("height", "100");
  loading_img.setAttribute("width", "100");
  var new_position = get_center_position({"height": 130, "width": 130});
  loading_div.style.position = "absolute";
  loading_div.style.zIndex = 2000;
  loading_div.style.top = new_position["margin-top"];
  loading_div.style.left = new_position["margin-left"];
  loading_div.appendChild(loading_img);
  return loading_div;
}

function find_city(){
  if(get_obj("find-city")){
    var city_button = get_obj("find-city");    
    city_button.addEventListener("click", function(e){load_req(e, "GET", process_city_req)}, false);
    var city_form = get_obj("city-search-form");
    city_form.addEventListener("focus", remove_text_from_input,  false);
  }
}

function get_url(e){
  if(e.target.id === "find-city"){
    var city_button = get_obj("find-city");
    var city_form = get_obj("city-search-form");
    var city_form_search = city_form.value;
    city_form_search = city_form_search.replace(",", "");
    var url = city_button.href + '?search=' + city_form_search;
  } else {
    url = e.target.href
  }
  return url;
}

function remove_text_from_input(event){
  this.oldvalue = this.value;
  this.value = "";
  this.addEventListener("blur", add_value_back, false);
}

function add_value_back(){
  if(this.value === ""){
    this.value = this.oldvalue;
  }
}

function change_url(object){
  var url = object.href;
  var segment = url.match('segment=[0-9][0-9]?');
  var segment_num = segment[0].match('[0-9][0-9]?');
  var new_segment_num = segment_num[0] * 1 + 1;
  url = url.replace(segment[0], "segment=" + new_segment_num);
  object.href = url;
}

function blank_the_search(){
  var search = document.getElementById("search-box");
  search.addEventListener("focus", remove_text_from_input,  false);
}

function get_more_reviews(){
  if(document.getElementById("get-more-reviews")){
    var get_reviews = document.getElementById("get-more-reviews");
    get_reviews.addEventListener("click", function(e){load_req(e, "GET", process_reviews_req, "")}, false);
  }
}

function setup_favorites(){
  if(document.getElementById("favorite-this")){
    var favoriter = document.getElementById("favorite-this");
    var todoer = document.getElementById("todo-this");
    var nastier = document.getElementById("nasty-this");
    nastier.addEventListener("click", function(e){load_req(e, "POST", process_favorites_req)}, false);
    favoriter.addEventListener("click", function(e){load_req(e, "POST", process_favorites_req)}, false);
    todoer.addEventListener("click", function(e){load_req(e, "POST", process_favorites_req)}, false);
  }
}

function get_center_position(size){
  var new_height = window.innerHeight / 2 - size["height"] / 2 + window.scrollY + "px";
  var new_width = window.innerWidth / 2 - size["width"] / 2 + window.scrollX + "px";
  return {"margin-top": new_height, "margin-left": new_width};
}

function switch_the_active_area(e){
  e.preventDefault();
  parent = e.target.parentNode;
  if(parent.id === "active"){
    return false;
  } else {
    var previous_active = get_obj("active");
    previous_active.id = "";
    previous_active = get_obj(previous_active.childNodes[0].id);
    var old_link_id = previous_active.id.replace("-link", "");
    var old_element = get_obj(old_link_id);
    removeClass(old_element, "active-element");
    addClass(old_element, "hidden-element");
    
    var link_id = e.target.id;
    e.target.parentNode.id = "active";
    link_id = link_id.replace("-link", "");
    var active_element = get_obj(link_id);
    addClass(active_element, "active-element");
    if(hasClass(active_element, "hidden-element")){
      removeClass(active_element, "hidden-element")
    }
  }
}

function setup_beer_details(){
  if(get_obj("details")){
    var review_form = get_obj("review");
    var reviews = get_obj("reviews");
    var details = get_obj("details");
    var review_link = get_obj("reviews-link");
    var details_link = get_obj("details-link");
    var form_link = get_obj("review-link");
    addClass(reviews, "hidden-element");
    addClass(review_form, "hidden-element");
    addClass(details, "active-element");
    review_link.addEventListener("click", function(e){switch_the_active_area(e);}, false);
    details_link.addEventListener("click", function(e){switch_the_active_area(e);}, false);
    form_link.addEventListener("click", function(e){switch_the_active_area(e);}, false);
  }
}


function addLoadEvent(func) {
  var oldonload = window.onload;
  if (typeof window.onload != 'function') {
    window.onload = func;
  } else {
    window.onload = function() {
      if (oldonload) {
        oldonload();
      }
      func();
    }
  }
};

addLoadEvent(blank_the_search);
addLoadEvent(get_more_reviews);
addLoadEvent(setup_favorites);
addLoadEvent(setup_beer_details);
addLoadEvent(find_city);