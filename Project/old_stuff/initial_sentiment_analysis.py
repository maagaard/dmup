#!/usr/bin/env python
# encoding: utf-8
import twitter
import nltk
import codecs
import happyfuntokenizing
from textblob import TextBlob



def analyze_tag(tag, tweet_count):
	tweets = twitter.get_timeline(tag, tweet_count)

	negatives = []
	positives = []
	indifferent = []

	for tweet in tweets:
		blob = TextBlob(tweet.text)
		polarity = blob.sentiment.polarity

		if polarity < -0.15:
			negatives += 1
		elif polarity > 0.15:
			positives.append(tweet.text)
		else:
			indifferent += 1

	print "Negs: " + str(negatives)
	print "Meehs: " + str(indifferent)
	print "Positives: " + str(len(positives))
	print positives


	return tweets



def do_analysis():
	tweets = twitter.get_timeline("swiftlang", 600)

	negatives = 0
	positives = []
	indifferent = 0

	for tweet in tweets:
		blob = TextBlob(tweet.text)
		polarity = blob.sentiment.polarity

		if polarity < -0.15:
			negatives += 1
		elif polarity > 0.15:
			positives.append(tweet.text)
		else:
			indifferent += 1

	print "Negs: " + str(negatives)
	print "Meehs: " + str(indifferent)
	print "Positives: " + str(len(positives))
	print positives


	return tweets


def do_nltk():
	tweets = twitter.get_timeline("swiftlang", 600)

	tokens = []
	for tweet in tweets:
		# tokens.extend(nltk.word_tokenize(tweet.text))
		tokenizer = happyfuntokenizing.Tokenizer(preserve_case=False)
		tokens.extend(tokenizer.tokenize(tweet.text))

	print len(tokens)

	write_to_file("tokens.txt", tokens)

	return tokens





def write_to_file(filename, tokens):
	with codecs.open(filename, 'w', "utf-8") as output_file:
		for token in tokens:
			output_file.write("%s\n" % token)

	# output_file.close()








if __name__ == '__main__':
	do_nltk()
	# do_analysis()
