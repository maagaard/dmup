import re, nltk


def segment_text():
	fid = open('string.txt', 'r')
	text = fid.read()
	fid.close()

	regex = re.compile("(\w+)")
	words = regex.findall(text)

	print words

	regex = re.compile("([.]\s[A-Z]?)")
	sentences = regex.split(text)

	print sentences

segment_text()