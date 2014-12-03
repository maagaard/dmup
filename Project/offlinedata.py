#!/usr/bin/env python
# encoding: utf-8
import json
import datetime
import codecs
from model import Tweet
from debug import DLOG



def test_data():

    pass


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
    # get_timeline("%23liverpool", 100)
    test_data()
