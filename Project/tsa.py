# import twitter
import sentimentanalyzer
from tweetfetcher import TweetFetcher


class TSA(object):
    """docstring for TwitterSentimentAnalyzer"""

    tsa = None
    tweet_fetcher = None

    def __init__(self):
        super(TSA, self).__init__()
        self.tsa = sentimentanalyzer.SentimentAnalyzer()
        self.tsa.load_classifier()
        self.tweet_fetcher = TweetFetcher()


    def analyze_hashtag(self, hashtag):
        # tweet_count = 1000

        # perhaps make a for loop ?
        # tweets = twitter.get_timeline("%23" + hashtag, tweet_count)

        tweets = self.tweet_fetcher.get_tweets(hashtag)

        self.tsa.clasify(tweets)
