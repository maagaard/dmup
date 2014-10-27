#!/usr/bin/env python
# encoding: utf-8
import twitterkeys
import json
import datetime
import codecs
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


def get_tweets_with_tag_and_max_id(client, tag, max_id):
	tag = "%23" + tag

	query = tag
	query += "&result_type=" + "recent"  # result_type
	if max_id is not None:
		query += "&max_id=" + str(max_id)
	query += "&count=" + str(MAX_TWEET_COUNT)

	request_start = datetime.datetime.now()
	response_json = client.request(twitter_api_url + query_tweets_url + query)  # Time consuming!!!
	print "request time: " + str(datetime.datetime.now() - request_start)

	response_dict = json.loads(json.dumps(response_json, sort_keys=True))
	search_metadata = response_dict['search_metadata']

	print "Query for " + tag
	print "query time: " + str(search_metadata['completed_in'])

	statuses = response_dict['statuses']

	tweets = []
	for status in statuses:
		tweet = Tweet(status)
		tweets.append(tweet)
		# print str(tweet.id) + ", " + tweet.created_at

		# print "Tweet: " + tweet.text
		# print "From user: " + tweet.user.name
		# print "Favorited: " + str(tweet.favorite_count)
		# print "Retweeted: " + str(tweet.retweet_count)

	new_max_id = tweets[-1].id
	return (tweets, new_max_id)


def get_timeline(search_tag):
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

		print loop_counter
		# print str(max_id) + ", " + str(new_max_id)

		if loop_counter == 3:
			break

		# write_tweets_to_file("test1.txt", timeline)
	return timeline


def write_tweets_to_file(filename, tweets):
	with codecs.open(filename, 'w', "utf-8") as file:
		for tweet in tweets:
			file.write("%s\n" % tweet.text)
	file.close()


if __name__ == '__main__':
	# get_tweets_with_tag("test_tag")
	get_timeline("liverpool")
