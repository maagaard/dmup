#!/usr/bin/env python
# encoding: utf-8
import twitter
import nltk
from textblob import TextBlob



def do_analysis():
	tweets = twitter.get_timeline("swiftlang")

	negatives = 0
	positives = 0
	indifferent = 0

	for tweet in tweets:
		blob = TextBlob(tweet.text)
		polarity = blob.sentiment.polarity
		if polarity < -0.15:
			negatives += 1
		elif polarity > 0.15:
			positives += 1
		else:
			indifferent += 1

	print "Pos: " + str(positives)
	print "Negs: " + str(negatives)
	print "Meehs: " + str(indifferent)

	return tweets


def do_nltk():
	tweets = twitter.get_timeline("swiftlang")

	tokens = []
	for tweet in tweets:
		tokens.extend(nltk.word_tokenize(tweet.text))

	print len(tokens)

	return tokens














if __name__ == '__main__':
	do_nltk()
	# do_analysis()
