install_scripts_env() {
  python -m pip install --user --upgrade pip
  pip install --user python-jenkins==0.4.16
  pip install --user dateutils==0.6.6
  pip install --user requests==2.22.0
  pip install --user requests-kerberos==0.11.0
  pip install --user httplib2==0.10.3
  pip install --user google-api-python-client==1.6.7
  pip install --user bugzilla==1.0.0
  pip install --user python-bugzilla==2.2.0
  pip install --user jira==2.0.0
  pip install --user paramiko==2.6.0
  pip install --user scp==0.13.2
  pip install --user confluence-py
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
  find /tmp  -name "*_content.txt" | xargs rm -rf {}
}
