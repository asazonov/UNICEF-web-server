var map;

function getInbox(){
	$(document).load('sample.json',function(data){ renderInbox(data); });
}

function renderInbox(data){
	
	// Parse to JSON
	JSONdata = $.parseJSON(data);
	
	// Create our map object
	
	
	$.each(JSONdata,function(key,value){
		// For each inbox item
		// Populate a property array
		//message[];
		$.each(value,function(key,value){
			message[key] = value;
			});
		// Now populate
		});
}

function initialize() {
        var mapOptions = {
          center: new google.maps.LatLng(4.8380, 31.5842),
          zoom: 12
        };
		map = new google.maps.Map(document.getElementById("mapoutput"),
            mapOptions);
		
		putonmarkers();
      }
	  
	  function putonmarkers(){
	  
	  var myLatlng = new google.maps.LatLng(4.8380,31.5842);
var marker = new google.maps.Marker({
position: myLatlng,
map: map,
icon: 'http://chart.apis.google.com/chart?chst=d_map_pin_letter&chld=1|FF0000|000000',
title:"Hello World!"
});

	var myLatlng2 = new google.maps.LatLng(10,1);
var marker2 = new google.maps.Marker({
position: myLatlng2,
map: map,
icon: 'http://chart.apis.google.com/chart?chst=d_map_pin_letter&chld=2|FF9900|000000',
title:"Hello World2!"
});

	  }


// Process the click event on the messages
$(document).ready(function(){
	setTimeout('initialize()',1000);
	$('#leftsidebar .item').click(function(){
		if($(this).attr('lat')!=null){
			newCenter = new google.maps.LatLng($(this).attr('lat'),$(this).attr('long'));
			map.setCenter(newCenter);
			map.setZoom(14);
		}
	});
});
