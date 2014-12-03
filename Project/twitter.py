#!/usr/bin/env python
# encoding: utf-8
import twitterkeys
import json
import datetime
import codecs
from application_only_auth import Client
from model import Tweet
from debug import DLOG


request_token_url = "https://twitter.com/oauth/request_token"
access_token_url = "https://twitter.com/oauth/access_token"
authorize_url = "https://twitter.com/oauth/authorize"
twitter_api_url = "https://api.twitter.com/1.1/"
query_tweets_url = "search/tweets.json?q="
query_user_timeline = "statuses/user_timeline.json?screen_name="

# Max number of tweets
MAX_TWEET_COUNT = 100


class TweetFetcher(object):
    """docstring for TweetFetcher"""

    twitter_client = None
    tweet_max_id = None

    def __init__(self):
        super(TweetFetcher, self).__init__()
        # self.arg = arg
        self.twitter_client = Client(twitterkeys.consumer_key, twitterkeys.consumer_secret)
        self.twitter_client._get_access_token()


    def get_client_status(self):
        status = self.twitter_client.rate_limit_status()
        return status['resources']['search']['/search/tweets']['remaining']


    def get_tweets_with_tag_and_max_id(self, search_tag, max_id):
        query = search_tag
        query += "%20lang%3Aen"
        query += "&result_type=" + "mixed"  # result_type
        if max_id is not None:
            query += "&max_id=" + str(max_id)
        query += "&count=" + str(MAX_TWEET_COUNT)

        request_start = datetime.datetime.now()  # request timing

        response_json = self.twitter_client.request(twitter_api_url + query_tweets_url + query)

        DLOG("Request time: " + str(datetime.datetime.now() - request_start))  # request timing

        response_dict = json.loads(json.dumps(response_json, sort_keys=True))
        statuses = response_dict['statuses']


        tweets = []
        for status in statuses:
            tweet = Tweet(status)
            tweets.append(tweet)

        if len(tweets) > 0:
            new_max_id = tweets[-1].id
            return (tweets, new_max_id)
        else:
            return (tweets, 0)


    def get_timeline(self, search_tag, length):

        max_id = None
        new_max_id = None
        loop_counter = 0

        timeline = []

        # Iterate over timeline
        while (loop_counter == 0) | (max_id != new_max_id):
            loop_counter += 1
            max_id = new_max_id - 1 if new_max_id is not None else None

            (new_tweets, new_max_id) = get_tweets_with_tag_and_max_id(search_tag, max_id)
            timeline.extend(new_tweets)

            # print str(max_id) + ", " + str(new_max_id)
            if len(timeline) >= length or new_max_id == 0:
                break

        return timeline


    def get_tweets(self, search_tag):
        query = search_tag
        query += "%20lang%3Aen"
        query += "&result_type=" + "mixed"  # result_type

        if self.tweet_max_id is not None:
            query += "&max_id=" + str(self.tweet_max_id)
        query += "&count=" + str(MAX_TWEET_COUNT)

        request_start = datetime.datetime.now()  # request timing

        response_json = self.twitter_client.request(twitter_api_url + query_tweets_url + query)

        DLOG("Request time: " + str(datetime.datetime.now() - request_start))  # request timing

        response_dict = json.loads(json.dumps(response_json, sort_keys=True))
        statuses = response_dict['statuses']
        # search_metadata = response_dict['search_metadata']

        tweets = []
        for status in statuses:
            tweet = Tweet(status)
            tweets.append(tweet)

        if len(tweets) > 0:
            self.tweet_max_id = tweets[-1].id
            return tweets
            # return tweets, search_metadata
        else:
            self.tweet_max_id = None
            return tweets


    def stop_fetching(self):
        self.tweet_max_id = None



################################### METHODS ####################################

def get_client_status():
    client = Client(twitterkeys.consumer_key, twitterkeys.consumer_secret)
    status = client.rate_limit_status()
    print status['resources']['search']['/search/tweets']['remaining']


def get_tweets_with_tag_and_period(tag, count, from_date, until_date):
    tag = "%23" + tag

    client = Client(twitterkeys.consumer_key, twitterkeys.consumer_secret)

    query = tag

    if from_date is not None:
        query += "+since%3A" + from_date

    if until_date is not None:
        query += "+until%3A" + until_date

    if count is not None:
        query += "&count=" + str(count)  # str(MAX_TWEET_COUNT)
    else:
        query += "&count=" + str(MAX_TWEET_COUNT)

    # tweets = client.request(twitter_api_url + query_tweets_url + query)
    response_json = client.request(twitter_api_url + query_tweets_url + query)
    response_dict = json.loads(json.dumps(response_json, sort_keys=True))
    search_metadata = response_dict['search_metadata']

    print "Query for " + tag
    print "query time: " + str(search_metadata['completed_in'])

    statuses = response_dict['statuses']

    tweets = []
    for status in statuses:
        tweet = Tweet(status)
        tweets.append(tweet)
        # print "Tweet: " + tweet.text
        # print "From user: " + tweet.user.name
        # print "Favorited: " + str(tweet.favorite_count)
        # print "Retweeted: " + str(tweet.retweet_count)
    return tweets


def get_tweets_with_tag(tag, count):
    return get_tweets_with_tag_and_period(tag, count, None, None)


def get_tweets_with_tag_and_max_id(client, tag, max_id):
    # filename = tag
    # tag = "%23" + tag

    query = tag
    query += "%20lang%3Aen"
    query += "&result_type=" + "mixed"  # result_type
    if max_id is not None:
        query += "&max_id=" + str(max_id)
    query += "&count=" + str(MAX_TWEET_COUNT)

    # request_start = datetime.datetime.now()


    # normal tweet search
    response_json = client.request(twitter_api_url + query_tweets_url + query)  # Time consuming!!!

    # print "request time: " + str(datetime.datetime.now() - request_start)

    response_dict = json.loads(json.dumps(response_json, sort_keys=True))
    # search_metadata = response_dict['search_metadata']

    # write_jsondata_to_file(filename, response_json)

    # print "Query for " + tag
    # print "query time: " + str(search_metadata['completed_in'])
    statuses = response_dict['statuses']


    ######## user timeline search #########
    # response_json = client.request(twitter_api_url + query_user_timeline + query)  # Time consuming!!!
    # statuses = response_dict


    tweets = []
    for status in statuses:
        tweet = Tweet(status)
        tweets.append(tweet)
        # print str(tweet.id) + ", " + tweet.created_at

        # print "Tweet: " + tweet.text
        # print "From user: " + tweet.user.name
        # print "Favorited: " + str(tweet.favorite_count)
        # print "Retweeted: " + str(tweet.retweet_count)

    if len(tweets) > 0:
        new_max_id = tweets[-1].id
        return (tweets, new_max_id)
    else:
        return (tweets, 0)


# def get_timeline(search_tag):
#   return get_timeline(search_tag, 100)

def get_timeline(search_tag, length):
    # now = datetime.datetime.now()
    # print now.date()
    client = Client(twitterkeys.consumer_key, twitterkeys.consumer_secret)
    client._get_access_token()

    max_id = None
    new_max_id = None
    loop_counter = 0

    timeline = []

    # Iterate over timeline
    while (loop_counter == 0) | (max_id != new_max_id):
        loop_counter += 1
        max_id = new_max_id - 1 if new_max_id is not None else None

        (new_tweets, new_max_id) = get_tweets_with_tag_and_max_id(client, search_tag, max_id)
        timeline.extend(new_tweets)

        # print str(max_id) + ", " + str(new_max_id)
        if len(timeline) >= length or new_max_id == 0:
            break

        # write_tweets_to_file("test1.txt", timeline)
    return timeline



def write_tweets_to_file(filename, tweets):
    with codecs.open(filename, 'w', "utf-8") as tweet_file:
        for tweet in tweets:
            tweet_file.write("-- \n%s\n" % tweet.text)
    tweet_file.close()


def write_jsondata_to_file(filename, data):
    with open(filename, 'w') as outfile:
        json.dump(data, outfile)


def read_json_from_file(filename):
    with open(filename, 'r') as data_file:
        return json.load(data_file)


def tweets_from_json(json_data):
    response_dict = json.loads(json.dumps(json_data, sort_keys=True))
    # search_metadata = response_dict['search_metadata']

    statuses = response_dict['statuses']

    tweets = []
    for status in statuses:
        tweet = Tweet(status)
        tweets.append(tweet)

    return tweets



def get_training_tweets():
    pos = []
    neg = []

    pos.extend(get_timeline("%23LFC%20%3A)", 100))
    pos.extend(get_timeline("%23manutd%20%3A)", 100))
    pos.extend(get_timeline("%23swiftlang%20%3A)", 100))
    pos.extend(get_timeline("%23StarWars%20%3A)", 100))
    # pos4 = get_timeline("kimkardashian%20%3A)", 100)
    # pos5 = get_timeline("cometlanding%20%3A)", 100)

    neg.extend(get_timeline("%23LFC%20%3A(", 100))
    neg.extend(get_timeline("%23manutd%20%3A(", 100))
    neg.extend(get_timeline("%23swiftlang%20%3A(", 100))
    neg.extend(get_timeline("%23StarWars%20%3A(", 100))
    # neg4 = get_timeline("kimkardashian%20%3A(", 100)
    # neg5 = get_timeline("cometlanding%20%3A(", 100)

    return {"pos": pos, "neg": neg}



def get_test_tweets():
    pos = []
    neg = []

    # pos_test = get_timeline("swiftlang%20%3A)", 100)
    # pos_test = get_timeline("kimkardashian%20%3A)", 100)
    # pos5 = get_timeline("cometlanding%20%3A)", 100)
    pos.extend(get_timeline("%23Ferguson%20%3A)", 100))

    # neg_test = get_timeline("swiftlang%20%3A(", 100)
    # neg_test = get_timeline("kimkardashian%20%3A(", 100)
    # neg5 = get_timeline("cometlanding%20%3A(", 100)
    neg.extend(get_timeline("%23Ferguson%20%3A(", 100))

    return {"pos": pos, "neg": neg}


def get_offline_tweets():

    pos1 = tweets_from_json(read_json_from_file("testdata/lfc_pos.json"))
    pos2 = tweets_from_json(read_json_from_file("testdata/manutd_pos.json"))
    neg1 = tweets_from_json(read_json_from_file("testdata/lfc_neg.json"))
    neg2 = tweets_from_json(read_json_from_file("testdata/manutd_neg.json"))


    return {"pos": pos1 + pos2, "neg": neg1 + neg2}


def get_offline_test_tweets():

    pos1 = tweets_from_json(read_json_from_file("testdata/starwars_pos.json"))
    neg1 = tweets_from_json(read_json_from_file("testdata/starwars_neg.json"))

    return {"pos": pos1, "neg": neg1}



def get_positive_training_data():
    pos = get_timeline("%3A)", 10000)
    write_tweets_to_file("postweets.txt", pos)


def get_objective_training_data():
    query_string = "reuters"
    objective = get_timeline(query_string, 10000)
    write_tweets_to_file("objectivetweets3.txt", objective)


def get_negative_training_data():
    neg = get_timeline("%3A(", 10000)
    write_tweets_to_file("negtweets.txt", neg)


if __name__ == '__main__':
    # get_tweets_with_tag("test_tag")
    get_timeline("%23liverpool", 100)
