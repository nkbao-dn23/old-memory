<?php
$array = array("Nam", "TRí", "Đức", "Tâm", "Lợi", "Phụng", "Thắng", "QUang");
  if(!isset($_COOKIE['id']))
    setcookie('id', '-1', time() + 3600,"/"); //3600 = 1hour
  else {
    $cookie = $_COOKIE['id'];
    switch($cookie){
      case '-1':
        break;
      case '8':
        $myfile = fopen("chall/chall1.txt", "r") or die("Unable to open file!");
        echo "<div class='alert alert-success' role='alert'>".fread($myfile,filesize("chall/chall1.txt"))." </div>";
        fclose($myfile);
        highlight_file("chall1.php");                         
        break;
      default:
        echo "<div class='alert alert-success' role='alert'>Chủ cookie là: ". $array[rand(0,7)] ." </div>";
        break;
    }
  }
?>