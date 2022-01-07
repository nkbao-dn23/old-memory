<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <meta name="description" content="">
    <meta name="author" content="">

    <title>PHP CHallenge</title>

    <!-- Font -->
    <link href="https://fonts.googleapis.com/css?family=Nunito:200,200i,300,300i,400,400i,600,600i,700,700i,800,800i,900,900i"
        rel="stylesheet">

     <!-- Bootstrap CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-1BmE4kWBq78iYhFldvKuhfTAU6auU8tT94WrHftjDbrCEXSU1oBoqyl2QvZ6jIW3" crossorigin="anonymous">
</head>

<body>
    <div class="container">
        <!-- Page Heading -->
        <h1>GIải các thử thách sau để mở HINTs cho CHallenge này</h1>
        <h4>(Các thử thách này chỉ mở ra các HINTs cho CHalenge, các bạn có thể giải hoặc không)</h4>
        <div id="chall1">
            <h4>CHallenge1: COOKIES troll</h4>
            <div class="code">
                <?php
                    require_once('chall1.php');
                ?>
            </div>
        </div>
        <div id="chall2">
            <h4>CHallenge 2: TRy to find the true password</h4>
            <form class="user" action="index.php" method="get">
                <input readonly value="@dm1n" class="form-control-plaintext">
                <br>
                <input type="password" id="pass" name="pass" placeholder="Password..." required class="form-control">
                <br>
                <button class="btn btn-primary">Đăng nhập</button>           
            </form>
            <div class="code">
                <?php
                    require_once('chall2.php');
                ?>
            </div>
        </div>
        <div id="chall3">
            <h4>CHallenge 3: Sort... sort... sort...</h4>
            <form class="user" action="index.php" method="get">
                <input id="str" name="str" placeholder="String..." required class="form-control">
                <br>
                <button class="btn btn-primary">Submit</button>
            </form>
            <br>
            <div class="code">
                <?php
                    require_once('chall3.php');
                ?>
            </div>
        </div>
    </div>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js" integrity="sha384-ka7Sk0Gln4gmtz2MlQnikT1wXgYsOg+OMhuP+IlRH9sENBO0LRn5q+8nbTov4+1p" crossorigin="anonymous"></script>
</body>
</html>