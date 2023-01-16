<?php 
    $page = basename($_SERVER['PHP_SELF']);
?>
<!-- Header -->
<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no" />
        <meta name="description" content="" />
        <meta name="author" content="" />
        <title>Neutrino UGR Group</title>
        <!-- Favicon
        <link rel="icon" type="image/x-icon" href="assets/favicon.ico" />-->
	<link rel="icon" type="image/x-icon" href="https://webmailest.ugr.es/skins/elastic/images/favicon.ico?s=1645187438">
        <!-- Font Awesome icons (free version)-->
        <script src="https://use.fontawesome.com/releases/v6.1.0/js/all.js" crossorigin="anonymous"></script>
        <!-- Google fonts-->
        <link href="https://fonts.googleapis.com/css?family=Montserrat:400,700" rel="stylesheet" type="text/css" />
        <link href="https://fonts.googleapis.com/css?family=Lato:400,700,400italic,700italic" rel="stylesheet" type="text/css" />
        <!-- Core theme CSS (includes Bootstrap)-->
        <link href="/test/css/styles.css" rel="stylesheet" />
    </head>
    <body id="page-top">
        <!-- Navigation-->
        <nav class="navbar navbar-expand-lg bg-secondary text-uppercase fixed-top" id="mainNav">
            <div class="container">
                <!--<a class="navbar-brand" href="#page-top">Neutrino UGR Group</a>-->
                <img src="assets/logo_white.png" class="navbar-brand" width="136" height="79" href="">
                <button class="navbar-toggler text-uppercase font-weight-bold bg-primary text-white rounded" type="button" data-bs-toggle="collapse" data-bs-target="#navbarResponsive" aria-controls="navbarResponsive" aria-expanded="false" aria-label="Toggle navigation">
                    Menu
                    <i class="fas fa-bars"></i>
                </button>
                <div class="collapse navbar-collapse" id="navbarResponsive">
                    <ul class="navbar-nav ms-auto">
                        <li class="nav-item mx-0 mx-lg-1"><a <?= ($page == 'research.php') ? 'class="nav-link py-3 px-0 px-lg-3 rounded page-item disabled page-item active' : 'class="nav-link py-3 px-0 px-lg-3 rounded' ?> href="/test/page/research.html">Research</a></li>
                        <li class="nav-item mx-0 mx-lg-1"><a <?= ($page == 'members.php') ? 'class="nav-link py-3 px-0 px-lg-3 rounded page-item disabled page-item active' : 'class="nav-link py-3 px-0 px-lg-3 rounded' ?> href="/test/page/members.html">Members</a></li>
			<li class="nav-item mx-0 mx-lg-1"><a <?= ($page == 'outreach.php') ? 'class="nav-link py-3 px-0 px-lg-3 rounded page-item disabled page-item active' : 'class="nav-link py-3 px-0 px-lg-3 rounded' ?> href="/test/page/outreach.html">Outreach</a></li>
			<li class="nav-item mx-0 mx-lg-1"><a <?= ($page == 'publications.php') ? 'class="nav-link py-3 px-0 px-lg-3 rounded page-item disabled page-item active' : 'class="nav-link py-3 px-0 px-lg-3 rounded' ?> href="/test/page/publications.html">Publications</a></li>
			<li class="nav-item mx-0 mx-lg-1"><a <?= ($page == 'talks.php') ? 'class="nav-link py-3 px-0 px-lg-3 rounded page-item disabled page-item active' : 'class="nav-link py-3 px-0 px-lg-3 rounded' ?> href="/test/page/talks.html">Talks</a></li>
			<li class="nav-item mx-0 mx-lg-1"><a <?= ($page == 'theses.php') ? 'class="nav-link py-3 px-0 px-lg-3 rounded page-item disabled page-item active' : 'class="nav-link py-3 px-0 px-lg-3 rounded' ?> href="/test/page/theses.html">Theses</a></li>
                        <li class="nav-item mx-0 mx-lg-1"><a class="nav-link py-3 px-0 px-lg-3 rounded" href="/wiki/index.php">Wiki</a></li>
                        <li class="nav-item mx-0 mx-lg-1"><a href="https://ugr.es"><img src="/assets/ugr_logo_2.jpg" class="navbar-brand" width="200" height="70"></a></li>
                    </ul>
                </div>
            </div>
        </nav>
