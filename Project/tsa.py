# import twitter
from sentimentanalyzer import SentimentAnalyzer
from tweetfetcher import TweetFetcher


class TSA(object):
    """docstring for TwitterSentimentAnalyzer"""

    sa = SentimentAnalyzer()
    tweet_fetcher = TweetFetcher()

    def __init__(self):
        super(TSA, self).__init__()
        self.sa.load_classifier()
        # self.tweet_fetcher = TweetFetcher()


    def analyze_hashtag(self, hashtag):
        # tweet_count = 1000

        # perhaps make a for loop ?
        # tweets = twitter.get_timeline("%23" + hashtag, tweet_count)

        tweets = self.tweet_fetcher.get_tweets(hashtag)

        analyzed_tweets = self.tsa.clasify(tweets)

        analyzed_tweets.sort(key=lambda x: datetime.datetime.strptime(x.tweet.created_at, '%Y-%m-%d'))

        
        for at in analyzed_tweets:
            .sort(key=lambda x: datetime.datetime.strptime(x['date'], '%Y-%m-%d'))