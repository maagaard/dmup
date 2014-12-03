import twitter
import sentimentanalyzer


class TSA(object):
    """docstring for TwitterSentimentAnalysis"""

    tsa = None

    def __init__(self):
        super(TSA, self).__init__()
        self.tsa = sentimentanalyzer.SentimentAnalyzer()
        self.tsa.load_classifier()


    def analyze_hashtag(self, hashtag):
        tweet_count = 1000
        tweets = twitter.get_timeline("%23" + hashtag, tweet_count)

        tsa.clasify(tweets)


