import tweetfetcher
from model import Tweet
from debug import DLOG
import codecs
import json
import datetime
import sentimentanalyzer as sa


def fetch_data(tag, count):

    fetcher = tweetfetcher.TweetFetcher()

    json_tweets = []
    for x in xrange(0, count / 100):
        json_tweets.extend(fetcher.get_tweets_as_json(tag)['statuses'])
        print "Tweets fetched: " + str(len(json_tweets))

    time_stamp = str(datetime.datetime.now())[:10]
    filename = tag + "-" + time_stamp
    write_jsondata_to_file(filename, json_tweets)


def analyze_tweets(filename):
    json_tweets = read_json_from_file(filename)
    tweets = tweets_from_json(json_tweets)
    SA = sa.SentimentAnalyzer()

    DLOG("Loaded " + str(len(tweets)) + " tweets")

    analyzed_tweets = []
    for x in xrange(0, len(tweets) / 100):
        analyzed_tweets.extend(SA.classify(tweets[(x * 100):(x + 1) * 100]))
        print "Tweets classified: " + str(len(analyzed_tweets))

    return analyzed_tweets


def write_jsondata_to_file(filename, data):
    with open(filename, 'w') as outfile:
        json.dump(data, outfile)


def read_json_from_file(filename):
    with open(filename, 'r') as data_file:
        return json.load(data_file)


def write_tweets_to_file(filename, tweets):
    with codecs.open(filename, 'w', "utf-8") as tweet_file:
        for tweet in tweets:
            tweet_file.write("-- \n%s\n" % tweet.text)
    tweet_file.close()


def tweets_from_json(json_data):
    # response_dict = json.loads(json.dumps(json_data, sort_keys=True))
    # statuses = response_dict['statuses']

    tweets = []
    for status in json_data:
        tweet = Tweet(status)
        tweets.append(tweet)

    return tweets


if __name__ == '__main__':
    fetch_data("%23Obama", 1000)
