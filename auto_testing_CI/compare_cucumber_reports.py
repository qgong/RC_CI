import talk_to_rc_jenkins_psi
import filecmp
import subprocess
import sys

class CompareCucumberReports():
  def __init__(self, username, password, build_name, new_report):
    self.ci_jenkins = talk_to_rc_jenkins_psi.TalkToRCCI(username, password, build_name)
    self.ci_jenkins.get_test_report_for_build()
    self.original_report= self.ci_jenkins.test_report[2]
    self.new_report = new_report

  def write_cucumber_report(self):
    download_report_1 = "curl --insecure -X GET -u {}:{} {} > new_report".format(username, password, self.new_report)
    download_report_2 = "curl --insecure -X GET -u {}:{} {} > original_report".format(username, password, self.original_report)
    subprocess.check_output(download_report_1, shell=True)
    subprocess.check_output(download_report_2, shell=True)

  def get_the_cases_num(self):
    new_cases_num_cmd = "grep -b12 '<tfoot' new_report | tail -n1 | cut -d '>' -f 2 | cut -d '<' -f 1 > new_num"
    old_cases_num_cmd = "grep -b12 '<tfoot' original_report | tail -n1 | cut -d '>' -f 2 | cut -d '<' -f 1 > original_num"
    subprocess.check_output(new_cases_num_cmd, shell=True)
    subprocess.check_output(old_cases_num_cmd, shell=True)

  def compare_cases_num(self):
    if filecmp.cmp('new_num','original_num'):
      print "Success! No change!"
    else:
      print "Attention! Cases changed, please update the cases groups of TS2 post merge CI!"

  def run_comparison(self):
    self.write_cucumber_report()
    self.get_the_cases_num()
    self.compare_cases_num()

if __name__ == "__main__":
  # print len(sys.argv)
  # print sys.argv
  username = sys.argv[1]
  password = sys.argv[2]
  build_name = sys.argv[3]
  report = sys.argv[4]
  compare_report = CompareCucumberReports(username, password, build_name, report)
  compare_report.run_comparison()
