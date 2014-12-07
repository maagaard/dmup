"""
dataminer.py is mainly intended for use by the authors
"""

__author__ = "Emil Maagaard & Bjarke Vad Andersen"
__credits__ = []
__version__ = "1.0"

import tweetfetcher
from model import Tweet
from debug import DLOG
import codecs
import json
import datetime
import sentimentanalyzer as sa
import cPickle


def fetch_data(tag, count):
    """
    Fetch tweets with hashtag.
    Hashtag and amount of tweets given as arguments.
    Nothing returned, tweets saved to json-file
    """
    fetcher = tweetfetcher.TweetFetcher()

    json_tweets = []
    for x in xrange(0, count / 100):
        json_tweets.extend(fetcher.get_tweets_as_json(tag)['statuses'])
        print "Tweets fetched: " + str(len(json_tweets))

    time_stamp = str(datetime.datetime.now())[:10]
    filename = tag + "-" + time_stamp
    write_jsondata_to_file(filename, json_tweets)


def analyze_tweets_from_file(filename):
    """
    Method intended for running "batch" analyzing jobs on tweets from file
    """
    json_tweets = read_json_from_file(filename)
    tweets = tweets_from_json(json_tweets)
    SA = sa.SentimentAnalyzer()
    SA.load_classifier()

    DLOG("Loaded " + str(len(tweets)) + " tweets")


    # for x in xrange(0, len(tweets) / 100):
    #     analyzed_tweets.extend(SA.classify(tweets[(x * 100):(x + 1) * 100]))
    #     print "Tweets classified: " + str(len(analyzed_tweets))

    analyzed_tweets = SA.classify(tweets)

    feature_file = filename + "-analyzed.pkl"
    with open(feature_file, "wb") as fid:
        cPickle.dump(analyzed_tweets, fid)

    return analyzed_tweets


def write_jsondata_to_file(filename, data):
    """
    Save json data to file with filename
    """
    with open(filename, 'w') as outfile:
        json.dump(data, outfile)


def read_json_from_file(filename):
    """
    Read json data from file with filename given as input
    """
    with open(filename, 'r') as data_file:
        return json.load(data_file)


def tweets_from_json(json_data):
    """
    Returns Tweet objects from json tweets
    """
    tweets = []
    for status in json_data:
        tweet = Tweet(status)
        tweets.append(tweet)

    return tweets


def write_tweets_to_file(filename, tweets):
    """
    Write tweet text to file.
    All tweets separated by new lines and "--"
    """
    with codecs.open(filename, 'w', "utf-8") as tweet_file:
        for tweet in tweets:
            tweet_file.write("-- \n%s\n" % tweet.text)
    tweet_file.close()


if __name__ == '__main__':
    fetch_data("%23Obama", 500)
