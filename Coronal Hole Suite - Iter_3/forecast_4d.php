<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <!-- The above 3 meta tags *must* come first in the head; any other head content must come *after* these tags -->
    <?php
		include "icon.php";
	?>
	
	<title>Dunedin Aurora - 4 Day Solar Wind Forecast</title>
	
	<script type="text/javascript" src="http://code.jquery.com/jquery-1.9.1.min.js"></script>
	<script type="text/javascript" src="http://code.highcharts.com/highcharts.js"></script>
	<script type="text/javascript" src="http://code.highcharts.com/modules/data.js"></script>

	<link href="https://fonts.googleapis.com/css?family=Raleway" rel="stylesheet">	
    <link href="css/bootstrap.min.css" rel="stylesheet">
	<link href="dna.css" rel="stylesheet">

    <!-- HTML5 shim and Respond.js for IE8 support of HTML5 elements and media queries -->
    <!-- WARNING: Respond.js doesn't work if you view the page via file:// -->
    <!--[if lt IE 9]>
      <script src="https://oss.maxcdn.com/html5shiv/3.7.3/html5shiv.min.js"></script>
      <script src="https://oss.maxcdn.com/respond/1.4.2/respond.min.js"></script>
    <![endif]-->
	

  </head>
  <body>
	<div class="container">
		<div class="page-header">
		<h1 class = "headline"><i>Dunedin Aurora</i></h1>
		</div>
		<?php
			include "menu.php";
		?>
		<!-- PAGE CONTENT HERE -->
		<h2>Coronal Hole Solar Wind Forecast <sub><a href="" data-toggle="modal" data-target="#modal_forecast">&sect;</a></sub></h2>
		<p>Based on <i>Empirical Space Weather Forecast Tool</i> by University of Graz.<br>SDO image courtesy of NASA/SDO and the AIA, EVE, and HMI science teams.</p>
		<p style = "color: red;"><b><i>BETA Test Edition</i></b></p>
		<div class = "row">
			<div class = "col-sm-4">
				<img class="img-responsive" src="sun.jpg">
				<p><i>SDO 193 &#8491; EUV Image</i><br>
			</div>
			<div class = "col-sm-4">
				<img class="img-responsive" src="syntopic.jpg">
				<p><i>NOAA SWPC Syntopic Map</i><br>
			</div>
			<div class = "col-sm-4">
				<img class="img-responsive" src="disc_full.bmp">
				<p><i>DunedinAurora.NZ computer generated CH Map</i><br>
			</div>
		</div>

		<!-- <div id="hss" style="width: 100%; height: 600px; margin: 0 auto"></div> -->
		<div class = "row">
			<br>
			<div class = "col-md-12">
				<button onclick="togglechart()">Toggle y-axis</button>
				<div id="forecast1"></div>
				<div id="forecast2"></div>
				<a href="" data-toggle="modal" data-target="#modal_scatterplot">Display scatterplot?</a>
			</div>
		</div>

<script type="text/javascript">
var chart1 = document.getElementById("forecast1");
var chart2 = document.getElementById("forecast2");
var chart_state = 1;

function state1()
{
	chart1.style.display = "block"; //display DIV
	chart2.style.display = "none"; // do not display DIV
}

function state2()
{
	chart1.style.display = "none"; // do not dislpay DIV
	chart2.style.display = "block"; // display DIV
}
function togglechart()
{
	if (chart_state == 1)
	{
		state2();
		chart_state = 2;
	}
	else if (chart_state == 2)
	{
		state1();
		chart_state = 1;
	}
};

state1();


var heightthing = 420;
		$(document).ready(function() {
			Highcharts.setOptions({})
			$.get('forecast.csv', function(csv) {
			    $('#forecast1').highcharts({
			        chart: {
			        	type: 'line',
						zoomType:'x',
						height: heightthing,
						spacingLeft: 10,
						spacingRight: 10,
						resetZoomButton: {
								position: {
									align: 'right', // right by default
									verticalAlign: 'top', 
									x: -20,
									y: 20
								},
								relativeTo: 'chart'
							}
			        },
					legend: {
						enabled: true
					},
					plotOptions: {
						series: {
							connectNulls: true,
							marker: {
								enabled: false
							}
						}
					},
					colors: ['#008000', '#ff0000'],
			        data: 
					{
			            csv: csv,
						//startColumn: 0,
						//endColumn: 1,
			        },
					series:[
						{
							visible: true,
							name: "Speed - Actual"
						},
						{
							visible: true,
							dashStyle: "shortdash",
							name: "Speed - Predicted",
							yAxis: 1
						}
					],
					tooltip: {
						enabled: true,
						crosshairs: true,
						shared: true
					},
			        title: 
					{
						text: 'Solar Wind Forecast - Split Y Axis'
					},
					subtitle:
					{
						text: 'DunedinAurora.NZ<br>Click and drag to zoom in'
					},
					yAxis: [
					{
						endOnTick: false,
						maxPadding: 0.1,
						minPadding: 0.1,
						tickInterval: 1,
						gridLineWidth: 1,
						gridLineColor: "#D8D8D8",
						title: 
							{
								text: 'Actual - km/s',
								style:
									{
										color: '#008000'
									},
							},
						labels: 
							{
								style:
								{
									color: "#008000"
								}
							}
					},
					{
						endOnTick: false,
						maxPadding: 0.1,
						minPadding: 0.1,
						tickInterval: 1,
						opposite: true,
						gridLineWidth: 0,
						title: 
							{
								text: 'Predicted - km/s',
								style:
									{
										color: '#ff0000'
									}
							},
						labels: 
							{
								style:
								{
									color: "#ff0000"
								}
							}
					}],

					xAxis: 
					{
						
						tickInterval: 24 * 3600 * 1000,
						minorTickInterval: 6 * 3600 * 1000,
						minorGridLineWidth: 1,
						minorGridLineColor: '#d8d8d8',
						gridLineWidth: 1,
						gridLineColor: "#a0a0a0",
						title: 
							{
								text: 'Date/Time UTC'
							},
						labels: 
							{
								style:
								{
									color: "#404040"
								}
							}
					}
			    });
			});
		});	

		$(document).ready(function() {
			Highcharts.setOptions({})
			$.get('forecast.csv', function(csv) {
			    $('#forecast2').highcharts({
			        chart: {
			        	type: 'line',
						zoomType:'x',
						height: heightthing,
						spacingLeft: 10,
						spacingRight: 10,
						resetZoomButton: {
								position: {
									align: 'right', // right by default
									verticalAlign: 'top', 
									x: -20,
									y: 20
								},
								relativeTo: 'chart'
							}
			        },
					legend: {
						enabled: true
					},
					plotOptions: {
						series: {
							connectNulls: true,
							marker: {
								enabled: false
							}
						}
					},
					colors: ['#008000', '#ff0000'],
			        data: 
					{
			            csv: csv,
						//startColumn: 0,
						//endColumn: 1,
			        },
					series:[
						{
							visible: true,
							name: "Speed - Actual"
						},
						{
							visible: true,
							dashStyle: "shortdash",
							name: "Speed - Predicted"
						}
					],
					tooltip: {
						enabled: true,
						crosshairs: true,
						shared: true
					},
			        title: 
					{
						text: 'Solar Wind Forecast - Single Y Axis'
					},
					subtitle:
					{
						text: 'DunedinAurora.NZ<br>Click and drag to zoom in'
					},
					yAxis: 
					{
						endOnTick: false,
						maxPadding: 0.1,
						minPadding: 0.1,
						tickInterval: 1,
						gridLineWidth: 1,
						gridLineColor: "#D8D8D8",
						title: 
							{
								text: 'Speed - km/s',
								style:
									{
										color: '#808080'
									},
							},
						labels: 
							{
								style:
								{
									color: "#808080"
								}
							}
					},

					xAxis: 
					{
						
						tickInterval: 24 * 3600 * 1000,
						minorTickInterval: 6 * 3600 * 1000,
						minorGridLineWidth: 1,
						minorGridLineColor: '#d8d8d8',
						gridLineWidth: 1,
						gridLineColor: "#a0a0a0",
						title: 
							{
								text: 'Date/Time UTC'
							},
						labels: 
							{
								style:
								{
									color: "#404040"
								}
							}
					}
			    });
			});
		});
		</script>	
		
		<?PHP
			include "regression.php";
			include "modal_forecast.php";
			include "modal_scatterplot.php";
		?>
		<footer>
		<?PHP
			include "footer.php";
		?>
		</footer>
		
		</div>
		<script src="js/bootstrap.min.js"></script>
  </body>
</html>