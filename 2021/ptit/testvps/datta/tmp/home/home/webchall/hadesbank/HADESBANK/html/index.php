<?php

ini_set('display_errors',0);
session_start();
include_once("db.php");
if ($db->connect_errno){
            die('Could not connect');
        }


@$user=$_GET['user'];
if (preg_match ("/drop|delete|update|insert|file_get_contents|select|=|limit|offset|substr|from|join|like|not|between|sleep|benchmark|\.|exec|where|in|>|<|-|having|as|all|;|show/i", $user))
{
        echo "<h1>SQLi detected</h1>"; 
}
else 
{
        $sql="select * from profile where Username='".$user."'";
        
        $result = $db->query($sql);
      


        echo '<br><br><br><div  class="" style="width:600px; margin: 0 auto; float: center;  "><br>'; 
        echo '<h1 style="color:#8A0886;text-align:center">💐Welcome To H4d3sbank💐</h1>';                        
        echo '<br><h2>You need "133333333333333333337 VNĐ" to get flag </h2>';
            
                while($row = $result->fetch_assoc()) {
                                echo "<h3 style=''>🧛‍You are <b style='color:red'> ".$row["Username"]." </b></h3> <br>"; 
                        echo "💵Your money: <i style='color:#04B404'>" . $row["Money"]." VNĐ</i><br>";
                        if($row["Money"]>=133333333333333333337){
                                echo "🌈✨NAI XỪ: ChristCTF{EzzSQL_Hades|-------Lo4DinG-----98%-----99%->❤️!!}✨";
                        }
                }
             echo "<br><a href='./users.php'>List users </a></br></br></div>";
        }
?>
