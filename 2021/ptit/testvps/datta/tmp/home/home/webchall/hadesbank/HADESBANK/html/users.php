<?php

ini_set('display_errors',0);
session_start();
include_once("db.php");
if ($db->connect_errno){
            die('Could not connect');
        }
$sql="select * from profile ";
$result = $db->query($sql);

echo '<br><br><br><div  class="" style="width:500px; margin: 0 auto; float: center;  "><br>'; 
echo '<h1 style="color:#8A0886;text-align:center">💐Welcome To H4d3sbank💐</h1>';
echo "<h2>📋List of customer problems: </h2><br>";
	 			echo "<table>";
	            echo "<tr>";
               
                echo "<th>Username</th>";
                echo "<th>Money</th>";
                
            	echo "</tr>";
        while($row = $result->fetch_assoc()) {
            echo "<tr>";
              
                echo "<td>" . $row['Username'] . "</td>";
                echo "<td>" . $row['Money'] . "</td>";
               
            echo "</tr>";
        }
        echo "</table>";
echo "</dir>";







				