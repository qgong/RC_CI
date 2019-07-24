# /bin/env python
# -*- coding: utf-8 -*-
import jenkins
import os
import sys

RC_Jenkins = os.environ.get(
    'RC_Jenkins_URL') or 'https://errata-jenkins.rhev-ci-vms.eng.rdu2.redhat.com'
Build_Job = 'deployment-packages'


class TalkToRCCIForLatestTargetBuild():
    def __init__(self, username, password, build_name=Build_Job):
        self.username = username
        self.password = password
        self.build_name = build_name
        self.server = jenkins.Jenkins(RC_Jenkins, self.username, self.password)
        self.target_build = ""
        self.target_branch = ""

    def get_builds_numbers(self):
        today_date = os.popen('date | cut -d " " -f 2-3').read().strip('\n')
        builds_numbers_cmd = "curl {}/job/{}/changes | grep -b1 \"({}\" | grep '#' | cut -d '#' -f 2".format(RC_Jenkins, self.build_name, today_date)
        write_builds_number_cmd = "{} > builds_numbers".format(builds_numbers_cmd)
        os.system(write_builds_number_cmd)

    def choose_the_target_build(self):
        # loop the builds_numbers to filter successful builds
        # if builds are more than 2, then get the branches of them
        # Once there is the release branch, let us choose the build id of the
        # release branch.
        builds_list = []
        success_builds = []
        success_builds_branches_map = {}
        with open('builds_numbers') as f:
            builds_list = f.readlines()

        if len(builds_list) == 0:
            print("There is no [success] builds today!")
            return 1

        for build in builds_list:
            build = int(build.strip('\n'))
            if self.server.get_build_info(self.build_name, build)['result'] == 'SUCCESS':
                success_builds.append(build)

        for build in success_builds:
            cmd = "curl -s {}/job/deployment-packages/{}/api/json?pretty=true | jq '.actions | .[] | select(._class ==\"hudson.model.ParametersAction\") | .parameters | .[] | select(.name ==\"GERRIT_BRANCH\") | .value' | sed 's/\"//g'".format(RC_Jenkins,build)
            branch = os.popen(cmd).read()
            success_builds_branches_map[build] = branch or 'release' 

        if 'release' in success_builds_branches_map.values():
            for build, branch in success_builds_branches_map.items():
                if branch == 'release':
                    self.target_build = build
                    self.target_branch = 'release'
                    break
        else:
            self.target_build = list(success_builds_branches_map.keys())[0]
            self.target_branch = 'develop'

    def run_to_get_the_target_build(self):
        self.get_builds_numbers()
        self.choose_the_target_build()


if __name__ == "__main__":
    username = sys.argv[1]
    password = sys.argv[2]
    if len(sys.argv) == 4:
        build_name = sys.argv[3]
        talk_to_rc_jenkins = TalkToRCCIForLatestTargetBuild(
            username, password, build_name)
    else:
        talk_to_rc_jenkins = TalkToRCCIForLatestTargetBuild(username, password)
    talk_to_rc_jenkins.run_to_get_the_target_build()
    print('{} of {}'.format(talk_to_rc_jenkins.target_build, talk_to_rc_jenkins.target_branch))
