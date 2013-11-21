$(document).ready(function(){
	var map = L.map('mapoutput');
	L.tileLayer('http://{s}.tile.cloudmade.com/42205C4BED464DCEABC785E965100D77/997/256/{z}/{x}/{y}.png', {
			maxZoom: 18
		}).addTo(map);
	var mapCentre = L.latLng(7.885,26.949)
	map.setView(mapCentre).setZoom(6);
});