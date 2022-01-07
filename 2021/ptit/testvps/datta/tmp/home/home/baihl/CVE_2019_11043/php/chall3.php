<?php
	function rand_str(){
		$str_array = 'abcdefghijklmnopqrstuvwsyz0123456789';
		$alphabet = str_split($str_array,1);

		$length = rand(20,26);

		$str = '';
		for ($i=0; $i<$length; $i++){
			$rand_num = rand($i, $length);
			$str = $str.$alphabet[$rand_num];
			$temp = $alphabet[$i];
			$alphabet[$i] = $alphabet[$rand_num];
			$alphabet[$rand_num] = $temp;
		}
		return $str;
	}

	if (!isset($_GET['str'])){
		$str = rand_str();
		echo "<h4 class='h3' style='color: blue; border: solid '>".$str."</h4>";
	}else{
		$input = $_GET['str'];
		if (strlen($input)<20)
			die ("<div class='alert alert-danger'>Chuỗi nhập sai!</div>");
		$input_array = str_split($input);
		for ($i=1; $i<strlen($input); $i++){
			if ($input_array[$i-1]>=$input_array[$i])
				die ("<div class='alert-danger'>Chuỗi nhập sai!</div>");			
		}
		$myfile = fopen("chall/chall3.txt", "r") or die("Unable to open file!");
	    echo "<div class='alert alert-success'>".fread($myfile,filesize("chall/chall3.txt"))." </div>";
	    fclose($myfile);
	}
	highlight_file("chall3.php");
?>