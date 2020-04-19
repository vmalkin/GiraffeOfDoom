<!DOCTYPE html>
<html lang="en">
<head>
<title>Dunedin Aurora</title>
<?php include "icon.php"; ?>
<?php include "head_content.php"; ?>
</head>

<body>
	<div id="container" class="col2-container">
	<!-- Header -->
		<header class="header">
			<?php include "banner.php"; ?>
		</header>
		
	<!-- navigation menu -->
		<nav class="nav">
			<?php
			include "menu.php";
			?>
		</nav>
	
	<!-- the following row div is needed if we are using css position -->
	<!-- instead of css-grid. REMOVE it if using grid -->
	<!-- <div class="row"> -->
	<!-- left column -->
		<div class="left">

		
		<div class="tile_row">
			<div class="tile">
				<div class="tile_heading">
				<h4>Geomagnetic Activity - 24hrs</h4>
				</div>
				<div class="tile_content highcharts">
					<?php
					include "spark_dna.php";
//include 'spark_newtrend.php';					
?>	
				</div>
			</div>
		</div>
			<div class="tile_row">
				<div class="tile">
					<div class="tile_heading">
					<h4>Solar Wind</h4>
					</div>
					<div class="tile_content">
						<?php
							include "spark_solarwind.php";
						?>
					</div>
				</div>
				
				<div class="tile">
					<div class="tile_heading">
					<h4>IMF</h4>
					</div>
					<div class="tile_content">
						<?php
						include "spark_bz.php";
						?>
					</div>
				</div>
			</div>
			<div class="tile_row">
				<div class="tile">
					<div class="tile_heading">
					<h4>Solar Wind Conditions & Forecast - 7 days</h4>
					</div>
					<div class="tile_content highcharts">
						<?php
						include "spark_4cast.php";
						?>
					</div>
				</div>
			</div>
		</div>
		
	<!-- right column -->
		<div class="right">
		<div class="tile_row">
			<div class="tile">
				<div class="tile_heading">
					<h4>Current Conditions</h4>
				</div>
				<div class="tile_content highcharts">
					<?php
					include "spark_status.php";
					?>	
				</div>
			</div>
		</div>
		<div class="tile_row">
			<div class="tile">
				<div class="tile_heading">
				<h4>Skycam</h4>
				</div>
				<div class="tile_content">
					<?php
						include "camera.php";
					?>
				</div>
			</div>
		</div>
		<div class="tile_row">
			<div class="tile">
				<div class="tile_heading">
				<h4>Lunar Phase</h4>
				</div>
				<div class="tile_content">
					<?php
						include "moonclock.php";
					?>
				</div>
			</div>
			
			<!-- <div class="tile"> -->
				<!-- <div class="tile_heading"> -->
				<!-- <h4>Ionosphere</h4> -->
				<!-- </div> -->
				<!-- <div class="tile_content"> -->

				<!-- </div> -->
			<!-- </div> -->
			
			<div class="tile_blank">
				<div class="tile_content">
					<p>&nbsp;
				</div>
			</div>
		</div>
		</div>
	<!-- the following row div is needed if we are using css position -->
	<!-- instead of css-grid. REMOVE it if using grid -->
	<!-- </div> -->
		
		
	<!-- footer -->
		<footer class="footer">
		<?php include "footer.php"; ?>
		</footer>
	</div>

</body>
</html>
