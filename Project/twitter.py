#!/usr/bin/env python
# encoding: utf-8
import twitterkeys
import json
from application_only_auth import Client
from model import Tweet


request_token_url = "https://twitter.com/oauth/request_token"
access_token_url = "https://twitter.com/oauth/access_token"
authorize_url = "https://twitter.com/oauth/authorize"
twitter_api_url = "https://api.twitter.com/1.1/"
query_tweets_url = "search/tweets.json?q="

# Max number of tweets
MAX_TWEET_COUNT = 100


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


if __name__ == '__main__':
	get_tweets_with_tag("test_tag")
