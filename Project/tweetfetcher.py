#!/usr/bin/env python
# encoding: utf-8
import twitterkeys
import json
import datetime
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


    def get_tweets(self, search_tag):
        query = search_tag
        query += "%20lang%3Aen"
        query += "&result_type=" + "mixed"  # result_types: "recent", "popular", "mixed"

        if self.tweet_max_id is not None:
            query += "&max_id=" + str(self.tweet_max_id - 1)
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



###############################   NOT NEEDED !?!?!?!  ###############################

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

            (new_tweets, new_max_id) = self.get_tweets_with_tag_and_max_id(search_tag, max_id)
            timeline.extend(new_tweets)

            # print str(max_id) + ", " + str(new_max_id)
            if len(timeline) >= length or new_max_id == 0:
                break

        return timeline
