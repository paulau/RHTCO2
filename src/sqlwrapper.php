<?php
	// This file generate output exactly in the same format, which 
	// was used hystorically with RHTCO2 loggers
	//echo $_GET["len"];
	$len = (int)$_GET["len"];
	//echo (string)$len;

	$tabelle = 'FAST'; 
	$MySQLServer = 'localhost';
	$MySQLNutzer = 'logger'; 
	$MySQLPass = 'logger112358'; 
	$MySQLDatabase = 'Datenerfassung';
		
	$conn = new mysqli($MySQLServer, $MySQLNutzer, $MySQLPass,  $MySQLDatabase);

	// Check connection
	if ($conn->connect_error) {
		die("Connection failed: " . $conn->connect_error);
		} 
	// select last element: 
	$sql = "SELECT * FROM FAST order by id limit " . (string)$len . ";";
	$result = $conn->query($sql);	
	
	if ($result->num_rows > 0) {
		// output data of each row
		while($row = $result->fetch_assoc()) {
			$date = date_create($row["Datum"]);			
			echo $date->format('d.m.Y') . " " . $row["Zeit"]. " " . $row["RH"] . "	" . $row["T"] . "	".  $row["CO2"]. "\r\n"; // 
			}
		} else {
		//echo "0 results";
		}
	$conn->close();	
	

?>
