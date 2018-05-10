install_scripts_env() {
  sudo pip install --upgrade pip
  sudo pip install confluence-py
  sudo pip install python-jenkins
  if [[ $(wget --version | head -1) =~ "GNU Wget" ]]; then
    echo "=====wget has been installed======";
  else
    echo "=====wget has not been installed, Would intall git======"
    sudo yum install wget -y
  fi
}
prepare_scripts(){
	mkdir -p ${1}
	cd ${1}
	echo "===============Download the CI files under $(pwd)=========="
	wget http://github.com/testcara/RC_CI/archive/master.zip
	unzip master.zip
	cd ${1}/RC_CI-master/auto_testing_CI
	# first check the page exists or not, if not, generate for all content
	echo "==============All files had beeen Download==============="
	echo "=============Firstly, let us check the page existing or not"
}
clean_env_mess(){
	sudo find /tmp  -name "*_content.txt" | xargs sudo rm -rf {}
}