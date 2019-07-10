import parser_build_testing_report
import talk_to_jenkins_to_send_report
import confluence_client
import sys


class TalkToJennkinsToParserResult():

  def __init__(self, confluence_username, confluence_password, et_build_version, title, space):
    self.confluence_username = confluence_username
    self.confluence_password = confluence_password
    self.et_build_version = et_build_version
    self.title = title
    self.space = space
    self.confluence_auto_client = confluence_client.ConfluenceClient(
        self.confluence_username, self.confluence_password, self.title, self.space, "", "")
    self.testing_report_content = ""
    self.testing_final_result = ""
    self.testing_final_summary = ""

  def get_testing_report_content(self):
    self.confluence_auto_client.get_page_content()
    self.testing_report_content = self.confluence_auto_client.content

  def parser_builds_report(self):
    build_parser = parser_build_testing_report.ParserBuildTestingReport(
        self.testing_report_content)
    build_parser.get_final_status_and_brief()
    self.testing_final_result = build_parser.final_result
    self.testing_final_summary = build_parser.brief_summary

  def run_parser(self):
    print "==== Getting the testing report content ===="
    self.get_testing_report_content()
    print "==== Parsering the build testing reprot ===="
    self.parser_builds_report()
    print self.testing_final_result
    print self.testing_final_summary
    print self.et_build_version


if __name__ == "__main__":
  confluence_username = sys.argv[1]
  confluence_password = sys.argv[2]
  et_build_version = sys.argv[3]
  title = sys.argv[4]
  space = sys.argv[5]
  parser = TalkToJennkinsToParserResult(
      confluence_username, confluence_password, et_build_version, title, space)
  parser.run_parser()
