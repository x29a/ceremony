<?php
ini_set('display_errors',1);
ini_set('display_startup_errors',1);
error_reporting(-1);

// configuration
$upload_dir = './uploads/';
$current_dir = './midi/';

function killPlayer()
{
  system('sudo killall python');
  system('sudo killall screen');
  system('sudo python /var/www/turnoff.py');
}

if(isset($_GET['r']))
{
  killPlayer();
  system('sudo reboot');
  header('Location: index.php');
}

if(isset($_GET['h']))
{
  killPlayer();
  system('sudo shutdown -hP now');
  header('Location: index.php');
}

if(isset($_GET['s']))
{
  killPlayer();
  header('Location: index.php');
}


if(isset($_GET['p']))
{
  killPlayer();
  system('sudo screen -dmS player python /var/www/player.py');
  header('Location: index.php');
}
?>

<!DOCTYPE html>
<html>
<body>

<?php
// check if a new current file should be set
if(isset($_GET['f']))
{
	if(isset($_GET['o']))
	{
		if($_GET['o'] == 'u')
		{
			if(file_exists($upload_dir.$_GET['f']))
			{
				// delete all files in player dir
				//array_map('unlink', glob($current_dir.'*'));

				// copy the file to the place where the player looks for a file
				if(!copy($upload_dir.$_GET['f'], $current_dir.$_GET['f']))
				{
					echo 'could not set a new current file<br/>';
				}
				else
				{
					header('Location: index.php');
				}
			}
		}
		else if($_GET['o'] == 'd')
		{
			// delete the file
			if(!unlink($upload_dir.$_GET['f']))
			{
				echo 'could not delete file<br/>';
			}
			else
			{
				header('Location: index.php');
			}
		}
		else if($_GET['o'] == 's')
		{
			// delete current file
			if(!unlink($current_dir.$_GET['f']))
			{
				echo 'could not delete current file</br>';
			}
			else
			{
				header('Location: index.php');
			}
		}
	}
}
?>
<hr>
<form action="upload.php" method="post" enctype="multipart/form-data">
    <input type="file" name="fileToUpload" id="fileToUpload">
    <input type="submit" value="Upload" name="submit">
</form>
<hr>
<?php
$current = glob($current_dir.'*');
echo '<u><b>Playlist</b></u><table width=100%>';
echo '<tr><td><b>name</b></td><td><b>size</b></td><td><b>delete</b></td></tr>';
foreach($current AS $file)
{
  $f = basename($file);
  echo'<tr><td>'.$f.'</td><td>'.filesize($file).'</td><td><a href="?f='.$f.'&o=s">delete</a></td>';
}
echo'</table>';
?>
<hr>
<?php
$files = glob($upload_dir.'*');
echo '<u><b>Storage</b></u><table width=100%>';
echo '<tr><td><b>name</b></td><td><b>size</b></td><td><b>use</b></td><td><b>delete</b></td></tr>';
foreach($files AS $file)
{
	$f = basename($file);
	echo'<tr><td><a href="'.$file.'">'.$f.'</a></td><td>'.filesize($file).'</td><td><a href="?f='.$f.'&o=u">add to playlist</a></td><td><a href="?f='.$f.'&o=d">delete</a></td>';
}
echo'</table>';
?>
<hr>
<a href="?r=true">reboot</a> - <a href="?h=true">shutdown</a> - <a href="?s=true">stop player</a> - <a href="?p=true">restart player</a>
</body>
</html>


