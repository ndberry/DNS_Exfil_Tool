<?PHP
require_once("./include/membersite_config.php");
?>

<!DOCTYPE html>
<!-- Template by Quackit.com -->
<!-- Images by various sources under the Creative Commons CC0 license and/or the Creative Commons Zero license. 
Although you can use them, for a more unique website, replace these images with your own. -->
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <!-- The above 3 meta tags *must* come first in the head; any other head content must come *after* these tags -->

    <title>Kittens!!</title>

    <!-- Bootstrap Core CSS -->
    <link href="css/bootstrap.min.css" rel="stylesheet">

    <!-- Custom CSS: You can use this stylesheet to override any Bootstrap styles and/or apply your own styles -->
    <link href="css/custom.css" rel="stylesheet">

    <!-- HTML5 Shim and Respond.js IE8 support of HTML5 elements and media queries -->
    <!-- WARNING: Respond.js doesn't work if you view the page via file:// -->
    <!--[if lt IE 9]>
        <script src="https://oss.maxcdn.com/libs/html5shiv/3.7.0/html5shiv.js"></script>
        <script src="https://oss.maxcdn.com/libs/respond.js/1.4.2/respond.min.js"></script>
    <![endif]-->

</head>

<body>

    <!-- Navigation -->
    <nav class="navbar navbar-default navbar-fixed-top" role="navigation">
        <div class="container">
            <!-- Logo and responsive toggle -->
            <div class="navbar-header">
                <button type="button" class="navbar-toggle" data-toggle="collapse" data-target="#navbar">
                    <span class="sr-only">Toggle navigation</span>
                    <span class="icon-bar"></span>
                    <span class="icon-bar"></span>
                    <span class="icon-bar"></span>
                </button>
                <a class="navbar-brand" href="#">
                	<span class="glyphicon glyphicon-fire"></span> 
                	NANOG KITTENS?
                </a>
            </div>
            <!-- Navbar links -->
            <div class="collapse navbar-collapse" id="navbar">
                <ul class="nav navbar-nav navbar-right">
                    <li class="active">
                        <a href="#">Home</a>
                    </li>
                    <li class="dropdown">
                        <a href="#" class="dropdown-toggle" data-toggle="dropdown" role="button" aria-haspopup="true" aria-expanded="false">Kittens <span class="caret"></span></a>
                            <ul class="dropdown-menu" aria-labelledby="about-us">
                                <li><a href="#">Siamese</a></li>
                                <li><a href="#">Persian</a></li>
                                <li><a href="#">Shorthair</a></li>
                                <li><a href="#">Mountain Lions</a></li>
                            </ul>
                   </li>
                   <li>
                       <a href="/DefConGui-1.jar">Get Cats On your Desktop!</a>
                   </li>
<?php
if($fgmembersite->CheckLogin())
{
    echo "<li class=dropdown>";
    echo "<a href=# class=dropdown-toggle data-toggle=dropdown role=button aria-haspopup=true aria-expanded=false>" . $fgmembersite->UserFullName() . "<span class=caret></span></a>";
    echo "<ul class=dropdown-menu aria-labelledby=about-us>";
    echo "<li><a href=/members.php>Member Page</a></li>";
    echo "<li><a href=/change-pwd.php>Change Password</a></li>";
    echo "<li><a href=/logout.php>Log Out</a></li>";
    echo "<li></li>";
    echo "</ul>";
    echo "</li>";
} else {
    echo "<li><a href=/login.php>Log In</a></li>";
    echo "<li><a href=/register.php>Create Account</a></li>";
}
?>
                    <li>
                        <a href="#"><span class="glyphicon glyphicon-shopping-cart"></span> My Cart</a>
                    </li>
                </ul>
            </div><!-- /.navbar-collapse -->
        </div><!-- /.container -->
    </nav>

	<!-- Feature -->
	<div class="jumbotron feature">
		<div class="container">
			<h1><span class="glyphicon glyphicon-equalizer"></span> Dramatically Engage</h1>
			<p>Objectively innovate empowered manufactured products whereas parallel platforms.</p>
			<p><a class="btn btn-primary" href="#">Engage Now</a></p>
		</div>
	</div>


    <!-- Heading -->
    <div class="container">
        <div class="row">
            <div class="col-xs-12">
                <h1 class="text-center">Superior Quality</h1>
                <p class="lead text-center">Proactively envisioned multimedia based expertise and cross-media growth strategies. Seamlessly visualize quality intellectual capital without superior collaboration and idea-sharing. Holistically pontificate installed base portals after maintainable products without collateral.</p>
            </div>
        </div>
    </div>

    <!-- Promos -->
	<div class="container-fluid">
        <div class="row promo">
        	<a href="#">
				<div class="col-md-4 promo-item item-1">
					<h3>
						Unleash
					</h3>
				</div>
            </a>
            <a href="#">
				<div class="col-md-4 promo-item item-2">
					<h3>
						Synergize
					</h3>
				</div>
            </a>
			
			<a href="#">
				<div class="col-md-4 promo-item item-3">
					<h3>
						Procrastinate
					</h3>
				</div>
            </a>
        </div>
    </div><!-- /.container-fluid -->

	<!-- Featured Products -->
	<div class="container">
		<h1 class="text-center">World Class Products</h1>
		<div class="row">
		
			<!-- Product 1 -->
			<div class="col-sm-6 col-md-3">
				<div class="thumbnail featured-product">
					<a href="#">
						<img src="images/pepper.jpg" alt="">
					</a>
					<div class="caption">
						<h3>Premium Niche</h3>
						<p>Nori grape silver beet broccoli kombu beet greens fava bean potato quandong celery. Bunya nuts black-eyed pea prairie turnip leek lentil turnip greens parsnip.</p>
						<p class="price">$10.45</p>

						<!-- Input Group -->
						<div class="input-group">
							<input type="number" class="form-control" value="1">
							<span class="input-group-btn">
								<button class="btn btn-primary" type="button">
									<span class="glyphicon glyphicon-shopping-cart" aria-hidden="true"></span> 
									Add to Cart
								</button>
							</span>
						</div>
					</div>
				</div>
			</div>

			<!-- Product 2 -->
			<div class="col-sm-6 col-md-3">
				<div class="thumbnail featured-product">
					<a href="#">
						<img src="images/jars.jpg" alt="">
					</a>
					<div class="caption">
						<h3>Handy Holistic</h3>
						<p>Nori grape silver beet broccoli kombu beet greens fava bean potato quandong celery. Bunya nuts black-eyed pea prairie turnip leek lentil turnip greens parsnip.</p>
						<p class="price"><s>$24.99</s> $18.99</p>

						<!-- Input Group -->
						<div class="input-group">
							<input type="number" class="form-control" value="1">
							<span class="input-group-btn">
								<button class="btn btn-primary" type="button">
									<span class="glyphicon glyphicon-shopping-cart" aria-hidden="true"></span> 
									Add to Cart
								</button>
							</span>
						</div>
					</div>
				</div>
			</div>

			<!-- Product 3 -->
			<div class="col-sm-6 col-md-3">
				<div class="thumbnail featured-product">
					<a href="#">
						<img src="images/pot.jpg" alt="">
					</a>
					<div class="caption">
						<h3>Seamless Strategic</h3>
						<p>Nori grape silver beet broccoli kombu beet greens fava bean potato quandong celery. Bunya nuts black-eyed pea prairie turnip leek lentil turnip greens parsnip.</p>
						<p class="price">$11.50</p>

						<!-- Input Group -->
						<div class="input-group">
							<input type="number" class="form-control" value="1">
							<span class="input-group-btn">
								<button class="btn btn-primary" type="button">
									<span class="glyphicon glyphicon-shopping-cart" aria-hidden="true"></span> 
									Add to Cart
								</button>
							</span>
						</div>
					</div>
				</div>
			</div>

			<!-- Product 4 -->
			<div class="col-sm-6 col-md-3">
				<div class="thumbnail featured-product">
					<a href="#">
						<img src="images/teapot.jpg" alt="">
					</a>
					<div class="caption">
						<h3>Maintained Strip</h3>
						<p>Nori grape silver beet broccoli kombu beet greens fava bean potato quandong celery. Bunya nuts black-eyed pea prairie turnip leek lentil turnip greens parsnip.</p>
						<p class="price">$45.50</p>

						<!-- Input Group -->
						<div class="input-group">
							<input type="number" class="form-control" value="1">
							<span class="input-group-btn">
								<button class="btn btn-primary" type="button">
									<span class="glyphicon glyphicon-shopping-cart" aria-hidden="true"></span> 
									Add to Cart
								</button>
							</span>
						</div>
					</div>
				</div>
			</div>
		</div>
    </div><!-- /.container -->
	
	
	<div class="container text-center">
		<h1>Unparalleled Service</h1>
		<p class="lead">Proactively envisioned multimedia based expertise and cross-media growth strategies. Seamlessly visualize quality intellectual capital without superior collaboration and idea-sharing. Holistically pontificate installed base portals after maintainable products without collateral.</p>
		<img class="img-responsive img-circle center-block" src="images/service.jpg" alt="">
	</div><!--/.container-->
	
		
	<!-- Footer -->
	<footer>
	
		<h1 class="text-center">Find Us</h1>
		<!-- Map -->
		<div class="footer-map"></div>	
			
			<div class="container">
				<div class="row">
					<div class="col-sm-12 footer-info-item text-center">
						<p class="lead">
							31 Spooner Street, Quahog, Rhode Island
						</p>
						<h2>Contact Us</h2>
						<p class="lead"><span class="glyphicon glyphicon-phone-alt"></span> +1(23) 456 7890<br>
						info@example.com</p>
					</div>
				</div>
			</div>

		<!-- Footer Links -->
		<div class="footer-info">
			<div class="container">
				<div class="row">
					<div class="col-sm-4 footer-info-item">
						<h3>Information</h3>
						<ul class="list-unstyled">
							<li><a href="#">About Us</a></li>
							<li><a href="#">Customer Service</a></li>
							<li><a href="#">Privacy Policy</a></li>
							<li><a href="#">Sitemap</a></li>
							<li><a href="#">Orders &amp; Returns</a></li>
						</ul>
					</div>
					<div class="col-sm-4 footer-info-item">
						<h3>My Account</h3>
						<ul class="list-unstyled">
							<li><a href="#">Sign In</a></li>
							<li><a href="#">View Cart</a></li>
							<li><a href="#">My Wishlist</a></li>
							<li><a href="#">Track My Order</a></li>
							<li><a href="#">Help</a></li>
						</ul>	
					</div>
					<div class="col-sm-4 footer-info-item">
						<h3><span class="glyphicon glyphicon-list-alt"></span> Newsletter</h3>
						<p>Sign up for exclusive offers.</p>
						<div class="input-group">
							<input type="email" class="form-control" placeholder="Enter your email address">
							<span class="input-group-btn">
								<button class="btn btn-primary" type="button">
									Subscribe!
								</button>
							</span>
						</div>
					</div>
				</div><!-- /.row -->
			</div><!-- /.container -->
        </div>
        
        <!-- Copyright etc -->
        <div class="small-print">
        	<div class="container">
        		<p><a href="#">Terms &amp; Conditions</a> | <a href="#">Privacy Policy</a> | <a href="#">Contact</a></p>
        		<p>Copyright &copy; Example.com 2015 </p>
        	</div>
        </div>
        
	</footer>

	
    <!-- jQuery -->
    <script src="js/jquery-1.11.3.min.js"></script>

    <!-- Bootstrap Core JavaScript -->
    <script src="js/bootstrap.min.js"></script>
	
	<!-- IE10 viewport bug workaround -->
	<script src="js/ie10-viewport-bug-workaround.js"></script>
	
</body>

</html>
