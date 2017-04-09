<html>
<head>
	<style>
	@keyframes tileanim
	{
		from {transform: rotateX(90deg); background-color: white;}
		to {transform: rotateX(0deg); }
	}
	table
	{
		width: 100%;
	}
	
	td
	{
		background-color: red;
		border-radius: 3px;
		-webkit-animation-name: tileanim; /* Safari 4.0 - 8.0 */
		animation-name: tileanim;
	}
	</style>
	
</head>

<body>

<?php 
include dna.php;
?>




</body>
</html>