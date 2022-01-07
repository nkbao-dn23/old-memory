<?php
	if(isset($_GET['pass'])){
		if (md5($_GET['pass'])=='0e124656823434657657655654324342'){
			$myfile = fopen("chall/chall2.txt", "r") or die("Unable to open file!");
	        echo "<div class='alert alert-success' role='alert'>".fread($myfile,filesize("chall/chall2.txt"))." </div>";
	        fclose($myfile);
		} else {
			echo "<div class='alert alert-danger' role='alert'>Sai password</div>";
		}
	}
	highlight_file("chall2.php");
?>