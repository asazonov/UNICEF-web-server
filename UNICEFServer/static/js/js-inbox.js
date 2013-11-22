var map;

function renderInbox(data) {
    // Map options
    var mapOptions = {
          center: new google.maps.LatLng(4.8380, 31.5842),
          zoom: 12
        };
	
	// Create our map object and incrementor
	map = new google.maps.Map(document.getElementById("mapoutput"),
            mapOptions);

	i = 1;
	
	$.each(data,function(key,value){
	    // Is there a location associated?
	    if(value.latitude){
	        // Yes
	        iconurl = 'http://chart.apis.google.com/chart?chst=d_map_pin_letter&chld='+i+'|FF0000|000000',
            new google.maps.Marker({
                icon:iconurl, 
                position: new google.maps.LatLng(value.latitude,value.longitude),
                map: map 
            });
            i++;
        }

        // Construct the item
        htmltoinsert = '<div class="item';
        // Danger and Local flags
        if(value.tag=="danger"){
            htmltoinsert += ' danger';
        }else if(value.tag=="local"){
            htmltoinsert += ' local';
        }
        // lat and long
        if(value.latitude){
            htmltoinsert+='" lat="'+value.latitude+'" long="'+value.longitude;
        }
        htmltoinsert += '">';
        
        // Insert iconurl if applicable
        if(iconurl){
            htmltoinsert += '<img class="map" src="'+iconurl+'"/>';
        }
        
        htmltoinsert += '<p class="from">'+value.sender_name+'</p>';
        htmltoinsert += '<p class="datetime">'+new Date(value.time_stamp*1000).toString()+'</p>';
        htmltoinsert += '<p class="body">'+value.body+'</p>';

        htmltoinsert += '</div>';

        $('#leftsidebar').append(htmltoinsert);

	});
}

function getInbox(){
	$.getJSON('/get_messages/', renderInbox);
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

$('#leftsidebar .item').click(function(){
    if($(this).attr('lat')!=null){
        newCenter = new google.maps.LatLng($(this).attr('lat'),$(this).attr('long'));
        map.setCenter(newCenter);
        map.setZoom(14);
    }
});


// Process the click event on the messages
$(document).ready(function(){
	setTimeout(
	    function() {
	        getInbox()
	    }, 1000
	);
});
