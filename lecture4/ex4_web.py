import requests
from lxml import etree

class WebExtraxt(dict):
	"""docstring for WebExtraxt"""
	def __init__(self, arg):
		super(WebExtraxt, self).__init__()
		self = web_extract()
		

def web_extract():
	url = ("http://www.kurser.dtu.dk/courses/02819/default.aspx?"
		"menulanguage=en-GB")

	url2 = ("http://karakterer.dtu.dk/Histogram/1/02819/Winter-2013")

	page = requests.get(url2).text
	html_parser = etree.HTMLParser(encoding='utf-8')
	xml_parser = etree.XMLParser(encoding='utf-8')
	root = etree.HTML(page)

	# print root.xpath('//tr/td//text()')
	# return {}

	# tables = [etree.XML(node) for node in root.xpath("//table")]
	# print tables
	list = [node.strip(' \r\n') for node in root.xpath('//tr/td//text()')]
	print list[5]
	return {}
	print [node.strip(' \r\n') for node in root.xpath('//tr/td//text()')]
	# print [etree.tostring(node, encoding='UTF-8', method='text').strip(',') for node in root.xpath('//tr/td//text()')]
	
	# fields = dict([[etree.tostring(child, encoding='UTF-8', method='text').strip(':') for child in node.getchildren()] for node in root.xpath("//tr[td/h3]")])
	fields = {}

	return fields

web_extract()