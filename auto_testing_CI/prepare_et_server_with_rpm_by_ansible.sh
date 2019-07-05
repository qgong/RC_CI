#!/bin/bash
set -eo pipefail

ET_Testing_Server=${ET_Testing_Server}
ET_Production_Server="errata.devel.redhat.com"
et_build_name_or_id=${et_build_name_or_id}
ansible_workspace=${WORKSPACE}/errata-tool-playbooks
ci_3_workspace=${WORKSPACE}

prepare_ansible_ssh_permission(){
  cp -rf /tmp/jenkins/.ssh /home/jenkins
  chmod 600 /home/jenkins/.ssh/*
  sed -i '/defaults]/a private_key_file = \/home\/jenkins\/.ssh\/id_rsa' ${ansible_workspace}/ansible.cfg
}

run_ansible(){
  set -x
  env
  #cd ${ansible_workspace}/playbooks/errata-tool
  cd ${ansible_workspace}/playbooks
  make clean-roles
  make qe-roles --ignore-errors
  e2e_env_workaround ${ET_Testing_Server} ${ansible_workspace}
  cd ../
  pwd
  echo ${1}
  sleep 3600
  ${1}
}

source ${ci_3_workspace}/RC_CI-master/auto_testing_CI/CI_Shell_prepare_env_and_scripts.sh
source  ${ci_3_workspace}/RC_CI-master/auto_testing_CI/CI_Shell_common_usage.sh
echo "---> Prepare the user ..."
ci-3-jenkins-slave
echo "---> whoami: $(whoami) ..."
echo "---> Prepare the ssh permision ..."
prepare_ansible_ssh_permission
echo "---> Prepare done ..."

# If you set the et build as empty, It would initail the ET version as the product version
if [[ -z "${et_build_name_or_id}" ]]; then
  echo "=== Et version is not specified. I would keep the deployed version is the product et version"
  product_raw_et_version=$(get_system_raw_version ${ET_Production_Server} | cut -d "-" -f 1)
  product_et_version=$(get_et_product_version ${ET_Production_Server})
  deployed_et_version=$(get_deployed_et_version ${ET_Testing_Server})
  echo "=== Get following versions:"
  echo "product et version: ${product_et_version}"
  echo "deployed et version: ${deployed_et_version}"
  compare_result=$(compare_version_or_id ${deployed_et_version} ${product_et_version})
  echo "compare_result: ${compare_result}"
  if [[ "${compare_result}" == "same" ]]; then
    echo "=== There is no need to deploy"
    echo "=== If the server is perf server, CI will restore the db and do db migration"
    perf_restore_db ${ET_Testing_Server}
    do_db_migration ${ET_Testing_Server}
    echo "=== Checking some specific setting again and restart service"
    update_setting ${ET_Testing_Server}
    restart_service ${ET_Testing_Server}
    exit
  else
    echo "=== I am initializing the testing server with the product version"
    ansible=$(get_ansible_commands_with_product_et_version ${ET_Testing_Server} ${product_raw_et_version} ${compare_result})
    echo "${ansible}"
    run_ansible "${ansible}"
    update_setting ${ET_Testing_Server}
    restart_service ${ET_Testing_Server}
    initialize_e2e_pub_errata_xmlrpc_settings
  fi
else
  # If you set the version, CI would compare the deployed version with the specfic version, then do actions accordingly.
  echo "=== ET version is specified, I would keep the deplyed version is the expected et version"
  deployed_et_id=$(get_deployed_et_id ${ET_Testing_Server})
  if [[ "${errata_fetch_brew_build}" == "true" ]]; then
    expected_et_id=${et_build_name_or_id}
  else
    expected_et_id=$(initial_et_build_id ${et_build_name_or_id})
  fi
  echo "=== Get following versions:"
  echo "expected version: ${expected_et_id}"
  echo "deployed et version: ${deployed_et_id}"
  compare_result=$(compare_version_or_id ${expected_et_id} ${deployed_et_id})
  echo "compare_result: ${compare_result}"
  if [[ "${compare_result}" == "same" ]]; then
    echo "There is no need to deploy"
    echo "=== If the server is perf server, CI will restore the db and do db migration"
    perf_restore_db ${ET_Testing_Server}
    do_db_migration ${ET_Testing_Server}
    echo "=== Checking some specific setting again and restart service"
    update_setting ${ET_Testing_Server}
    restart_service ${ET_Testing_Server}
    exit
  else
    product_raw_et_version=$(get_system_raw_version ${ET_Production_Server} | cut -d "-" -f 1)
    product_et_version=$(get_et_product_version ${ET_Production_Server})
    deployed_et_version=$(get_deployed_et_version ${ET_Testing_Server})
    echo "=== Get following versions:"
    echo "product version: ${product_et_version}"
    echo "deployed et version: ${deployed_et_version}"
    compare_result=$(compare_version_or_id ${deployed_et_version} ${product_et_version})
    echo "compare_result: ${compare_result}"
    if [[ "${compare_result}" == "same" ]]; then
      echo "=== There is no need to redeploy et as product et version"
    else
      echo "=== Before upgrade the expected version, I will initialize the testing server as et product version"
      perf_restore_db ${ET_Testing_Server}
      ansible=$(get_ansible_commands_with_product_et_version ${ET_Testing_Server} ${product_raw_et_version} ${compare_result})
      echo "${ansible}"
      run_ansible "${ansible}"
    fi
    echo "=== Upgrade to the current expected et version"
    if [[ "${errata_fetch_brew_build}" == "false" ]]; then
      ansible=$(get_ansible_commands_with_build_id ${ET_Testing_Server} ${expected_et_id})
    else
      ansible=$(get_ansible_commands_with_brew_build_id ${ET_Testing_Server} ${expected_et_id})
    fi
    echo "${ansible}"
    run_ansible "${ansible}"
    update_setting ${ET_Testing_Server}
    restart_service ${ET_Testing_Server}
    initialize_e2e_pub_errata_xmlrpc_settings
  fi
fi
