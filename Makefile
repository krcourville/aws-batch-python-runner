# deploy assumes a symbolic link "tf.exe" in the path to "terraform.exe"
deploy:
	echo "test"
	cd infrastructure && tf apply -auto-approve
