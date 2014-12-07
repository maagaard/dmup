#!/usr/bin/env python
# encoding: utf-8

__author__ = "Emil Maagaard & Bjarke Vad Andersen"
__credits__ = []
__version__ = "1.0"

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
    """
    TweetFetcher
    Class for fetching tweets
    """

    twitter_client = None
    tweet_max_id = None

    def __init__(self):
        super(TweetFetcher, self).__init__()
        self.twitter_client = Client(twitterkeys.consumer_key, twitterkeys.consumer_secret)
        self.twitter_client._get_access_token()


    def get_client_status(self):
        """
        Returns the remaining amount of tweet queries available for the current 15 minute period.
        """
        status = self.twitter_client.rate_limit_status()
        return status['resources']['search']['/search/tweets']['remaining']


    def get_tweets_as_json(self, search_tag):
        """
        Returns 100 tweets containing the search hashtag as a json dictionary
        """
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

        if len(response_dict['statuses']) > 0:
            self.tweet_max_id = response_dict['statuses'][-1]['id']
        else:
            self.tweet_max_id = None

        return response_dict


    def get_tweets(self, search_tag):
        """
        Returns 100 tweets containing the search hashtag as Tweet objects
        """
        response_dict = self.get_tweets_as_json(search_tag)
        statuses = response_dict['statuses']
        # search_metadata = response_dict['search_metadata']

        tweets = []
        for status in statuses:
            tweet = Tweet(status)
            tweets.append(tweet)

        return tweets


    def get_newest(self, search_tag, id):
        """
        Method for updating timeline.

        """
        raise NotImplementedError


    def stop_fetching(self):
        """
        Resets max id so that any query will start from "scratch"
        """
        self.tweet_max_id = None
