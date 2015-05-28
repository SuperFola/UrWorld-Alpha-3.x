<!DOCTYPE HTML>
<html>
	<head>
		<meta charset="utf-8" />
		<title>UrWorld - Jeu 2D en Python</title>
		<link rel="stylesheet" type="text/css" href="css/design.css" />
		<meta name="google-site-verification" content="WnEZtlHK_G_zftfiHq7Aw9ywm5D4stXY02lbB6qSIRE" />
	</head>
	<body>
		<div id="logo">
			<img src="images/logo.png" alt="Logo UrWorld par Neoblast1996"/>
		</div>
		<div id="content">
			<center>
				<h1>Register your version of UrWorld !</h1>
			</center>
			<br>
			<br>
			<br>
			<center>
				<form method="post" action="register.php" enctype="multipart/form-data">
					Pseudo : <input type="text" name="cle" placeholder="Folaefolc"/>
					<br>
					E-Mail (facultatif) : <input type="text" name="email" placeholder="example@my_host.fr">
					<br>
					<input type="submit" name="go!" value = "Go !"/>
				</form>
			</center>
			<?php
			if (isset($_POST['cle']) AND isset($_POST['email']))
				{
					$les_cles = fopen('register.txt', 'a+');
					$valeur = $_POST['cle'] . ' - ';
					fputs($les_cles, $valeur);
					fclose($les_cles);
					
					if (isset($_POST['email']) AND $_POST['email'] != NULL)
						{
							$email_ = fopen('email.txt', 'r+');
							$utilisateur = $_POST['email'] . " : " . $_POST['cle'] . " - ";
							fseek($email_, 0);
							fputs($email_, $utilisateur);
							fclose($email_);
						}
					?>
					<font color=#568203><center><h1>
					<?php
					echo "Opération d'ajout réussie !";
				}
			?>
			</h1></center></font>
		</div>
	</body>
</html>