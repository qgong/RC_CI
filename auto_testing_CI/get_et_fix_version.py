#!/bin/env python
import os
import sys
JIRA_URL = "https://docs.engineering.redhat.com/display/Errata/Errata+Tool+Release+Plans"

class GetFixVersion():
    def __init__(self, confluence_user, confluence_password):
        self.confluence_user = confluence_user
        self.confluence_password = confluence_password
        self.current_release = ""
        self.current_fix_version = ""

    def get_the_releases_page_content(self):
        get_release_page_content_cmd = 'curl -o release_page_content -u {}:{} {}'.format(self.confluence_user, self.confluence_password, JIRA_URL)
        os.system(get_release_page_content_cmd)

    def get_the_release(self):
        get_release_versions_list_cmd = "grep -o 'ET [0-9.-]\+\? Release Plan' release_page_content | tr -d '[ a-zA-Z]' | head -n1"
        self.current_release = os.popen(get_release_versions_list_cmd).read()
        self.current_release = self.current_release.strip('\n')

    def get_the_fix_version(self):
        if self.current_release.find('-0') < 0:
            self.current_fix_version = "{}-0".format(self.current_release)

    def run(self):
        self.get_the_releases_page_content()
        self.get_the_release()
        self.get_the_fix_version()

if __name__ == "__main__":
    username = sys.argv[1]
    password = sys.argv[2]
    GetVersion = GetFixVersion(username, password)
    GetVersion.run()
    print(GetVersion.current_fix_version)
