from sentimentanalyzer import SentimentAnalyzer
from tweetfetcher import TweetFetcher


def sort_tweets(tweets):
    tweets.sort(key=lambda x: x.get_date())
    return tweets



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

        tweets = self.tweet_fetcher.get_tweets(hashtag)
        analyzed_tweets = sort_tweets(self.sa.classify(tweets))


        if len(analyzed_tweets) < 500:
            bin_size = 10
        else:
            bin_size = int(len(analyzed_tweets) * .02)

        bins = []
        for count in range(int(len(analyzed_tweets) / bin_size)):
            pol_bin = [tweet.polarity for tweet in analyzed_tweets[count:(count + bin_size)]]
            bins.append(pol_bin)
            count += bin_size

        print [sum(bin) for bin in bins]
