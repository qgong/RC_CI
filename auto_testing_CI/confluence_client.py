import sys
import ci3_error
from confluence import Api
class ConfluenceClient():
	def __init__(self, username, password, title, space, content, parent_page):
		wiki_url = "https://docs.engineering.redhat.com"
		self.api = Api(wiki_url, username, password)
		self.page_name = title
		self.general_content = content
		self.space = space
		self.parent_page = parent_page
		self.content = ""

	def create_update_page(self):
		self.get_page_content()
		if self.content.find("it does not exist.") > 0 or self.content.find("table") < 0 :
			print "==== Will add page ==="
			self.api.addpage(self.page_name, self.space, self.general_content, parentpage=self.parent_page)
		else:
			print "==== Will update page ==="
			self.api.updatepage(self.page_name, self.space, self.general_content, self.parent_page, label="CI_3_Testing")

	def get_page_content(self):
		try:
			self.content = self.api.getpagecontent(self.page_name, self.space)
		except Exception, error:
			self.content = str(error)


if __name__ == "__main__":
	get_page = "false"
	create_update_page = "false"
	if len(sys.argv) == 5:
		get_page = "true"
	elif len(sys.argv) == 7:
		create_update_page = "true"
	else:
		raise ci3_error.ConfulenceClientInputError()

	username = sys.argv[1]
	password = sys.argv[2]
	title = sys.argv[3]
	space = sys.argv[4]
	if get_page == "true":
		confulence_client = ConfluenceClient(username, password, title, space, "", "")
		confulence_client.get_page_content()
	if create_update_page == "true":
		content = sys.argv[5]
		parentpage = sys.argv[6]
		confulence_client =  ConfluenceClient(username, password, title, space, content, parentpage)
		confulence_client.create_update_page()
