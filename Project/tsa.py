import datetime
from sentimentanalyzer import SentimentAnalyzer
from tweetfetcher import TweetFetcher


def sort_tweets(tweets):
    return tweets.sort(key=lambda tweet: tweet.get_date())



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

        analyzed_tweets = self.sa.classify(tweets)


        for x in xrange(0, 15):
            print str(analyzed_tweets[x].get_date())

        print "--------------"

        analyzed_tweets.sort(key=lambda x: x.get_date())

        for x in xrange(0, 15):
            print str(analyzed_tweets[x].get_date())

        return analyzed_tweets



        for at in analyzed_tweets:
            # .sort(key=lambda x: datetime.datetime.strptime(x['date'], '%Y-%m-%d'))
            pass

        for tweet in analyzed_tweets:

            pass


        if len(analyzed_tweets) < 500:
            bin_size = 10

            for count in range(len(analyzed_tweets) / bin_size):
                pol_sum = [sum(tweet.polarity) for tweet in analyzed_tweets[count:(count + bin_size)]]
                print pol_sum

            pass

        else:

            pass
