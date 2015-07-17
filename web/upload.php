<?php
$target_dir = "uploads/";
$target_file = $target_dir . basename($_FILES["fileToUpload"]["name"]);
$uploadOk = 1;
$imageFileType = pathinfo($target_file,PATHINFO_EXTENSION);

// Check if file already exists
if (file_exists($target_file)) {
    	if(!unlink($target_file))
	{
		echo'could not delete existing file';
		$uploadOk = 0;
	}
}

// Check if $uploadOk is set to 0 by an error
if ($uploadOk) {
    if (move_uploaded_file($_FILES["fileToUpload"]["tmp_name"], $target_file)) {
   	header('Location: index.php'); 
    } else {
        echo "Sorry, there was an error uploading your file.";
    }
}
?>
