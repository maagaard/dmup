# import oauth2 as oauth
# import urlparse
# import webbrowser
import twitterkeys
import json
from application_only_auth import Client

request_token_url = "https://twitter.com/oauth/request_token"
access_token_url = "https://twitter.com/oauth/access_token"
authorize_url = "https://twitter.com/oauth/authorize"
twitter_api_url = "https://api.twitter.com/1.1/"
query_tweets_url = "search/tweets.json?q="

# Max number of tweets
MAX_TWEET_COUNT = 1


def access_twitter():

	client = Client(twitterkeys.consumer_key, twitterkeys.consumer_secret)

	# "search?q=%23liverpool%20since%3A2014-10-20&src=typd"

	query_tag = "%23liverpool"
	start_date = "2014-10-01"
	end_date = "2014-10-14"
	result_type = "recent"
	count = str(MAX_TWEET_COUNT)

	query_string = query_tag

	if start_date != "":
		query_string += "+since%3A" + start_date

	if end_date != "":
		query_string += "+until%3A" + end_date

	if count != "":
		query_string += "&count=" + count

	if result_type != "":
		query_string += "&result_type=" + result_type


	response_json = client.request(twitter_api_url + query_tweets_url + query_string)
	# print json.dumps(response_json, sort_keys=True, indent=4, separators=(',', ':'))

	response_dict = json.loads(json.dumps(response_json, sort_keys=True))
	search_metadata = response_dict['search_metadata']

	print "Query for " + query_tag
	print "query time: " + str(search_metadata['completed_in'])

	statuses = response_dict['statuses']

	for status in statuses:
		print status['text']



	# consumer = oauth.Consumer(key=twitterkeys.consumer_key, secret=twitterkeys.consumer_secret)
	# client = oauth.Client(consumer)
	# response, content = client.request(request_token_url, "GET")
	# request_token = dict(urlparse.parse_qsl(content))
	# url = "%s?oauth_token=%s" % (authorize_url, request_token["oauth_token"])
	# webbrowser.open(url)
	# token = oauth.Token(request_token["oauth_token"], request_token["oauth_token_secret"])

	# token.set_verifier(oauth_verifier)
	# client = oauth.Client(consumer, token)
	# response, content = client.request(access_token_url, "POST")


def get_tweets_with_tag(tag):
	tag = "%23" + tag

	client = Client(twitterkeys.consumer_key, twitterkeys.consumer_secret)
	query = tag + "&count=" + MAX_TWEET_COUNT
	tweets = client.request(twitter_api_url + query_tweets_url + query)

	print json.dumps(tweets, sort_keys=True, indent=4, separators=(',', ':'))



if __name__ == '__main__':
	access_twitter()
