install_scripts_env() {
  pip install --user --upgrade pip
  pip install --user confluence-py
  pip install --user python-jenkins
  pip install --user dateutils
  pip install --user requests
  pip install --user requests_kerberos
  pip install --user httplib2
  pip install --user google-api-python-client
  pip install --user bugzilla
  pip install --user python-bugzilla
  pip install --user jira
  pip install --user paramiko
  pip install --user scp
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
