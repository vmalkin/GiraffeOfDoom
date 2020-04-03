<script>
var active_speed = 500;
var active_density = 10;
var colour_warning = "#f03030";

$.getJSON("dnacore/sw_speed.json", function(jsondata){
	$("#value_speed").text(jsondata.data);
	var timedata = new Date(jsondata.posix_time * 1000);
	var hr = timedata.getUTCHours();
	if (hr.length < 2)
	{
		hr = "0" + hr;
	}
	
	var mn = timedata.getUTCMinutes();
	if (mn.length < 2)
	{
		mn = "0" + mn;
	}
	
	var timestamp = hr + ":" + mn + " UTC";
	
	$("#sp_time").text(timestamp);
	
	if (jsondata.data > active_speed)
	{
		$("#sw_speed").css("background-color", colour_warning);
	}
});

$.getJSON("dnacore/sw_density.json", function(jsondata){
	var timedata = new Date(jsondata.posix_time * 1000);
	var hr = timedata.getUTCHours();
	if (hr.length < 2)
	{
		hr = "0" + hr;
	}
	
	var mn = timedata.getUTCMinutes();
	if (mn.length < 2)
	{
		mn = "0" + mn;
	}
	
	var timestamp = hr + ":" + mn + " UTC";
	
	$("#ds_time").text(timestamp);
	
	$("#value_density").text(jsondata.data);
	
		if (jsondata.data > active_density)
	{
		$("#sw_density").css("background-color", colour_warning);
	}
});

</script>

<table style="width: 100%; margin-left: auto; margin-right: auto;">
<tr>
	<th>Speed</th>
	<th>Density</th>
</tr>
<tr>
	<td><sub><span id="sp_time">timestamp</span></sub></td>
	<td><sub><span id="ds_time">timestamp</span></sub></td>
</tr>
<tr>
	<td id="sw_speed" style="background-color: lightgreen;"><span id="value_speed"></span> km/s</td>
	<td id="sw_density" style="background-color: lightgreen;"><span id="value_density"></span> p/m<sup>3</sup>
</tr>
</table>