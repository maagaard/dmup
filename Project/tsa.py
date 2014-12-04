from sentimentanalyzer import SentimentAnalyzer
from tweetfetcher import TweetFetcher
from debug import DLOG


import numpy as np
import numpy.random
import matplotlib.pyplot as plt


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


        tweets = []
        # for x in xrange(1, 10):
        tweets.extend(self.tweet_fetcher.get_tweets(hashtag))

        analyzed_tweets = sort_tweets(self.sa.classify(tweets))
        # analyzed_tweets = sort_tweets(self.sa.classify(tweets))


        if len(analyzed_tweets) < 500:
            bin_size = 10
        else:
            bin_size = int(len(analyzed_tweets) * .02)

        bins = []
        for count in range(0, int(len(analyzed_tweets) / bin_size)):
            pol_bin = [tweet.polarity for tweet in analyzed_tweets[(count * bin_size):((count + 1) * bin_size)]]
            bins.append(pol_bin)


        DLOG([sum(bin) for bin in bins])

        plt.boxplot(bins)
        plt.show()


        # plt.xticks(range(1, 11), bin_nums)

        # print [(sum(bin) / bin_size) for bin in bins]

        # numbers = [(sum(bin) / bin_size) for bin in bins]

        # bin_nums = [bins.index(bin) for bin in bins]

        # plt.figure(1)


        # # plt.bar([-1, -0.5, 0, 0.5, 1], ((sum(bin) / bin_size) for bin in bins))

        # # plt.hist([(sum(bin) / bin_size) for bin in bins], bins=bin_nums)

        # # (array([0, 2, 1]), array([0, 1, 2, 3]), <a list of 3 Patch objects>)
        # plt.show()

        # # np.histogram(bins, bins=len(bins))

        # # heatmap, xedges, yedges = np.histogram2d(x, y, bins=50)
        # # extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]

        # # plt.clf()
        # # plt.imshow(heatmap, extent=extent)
        # # plt.show()



if __name__ == '__main__':
    TSA = TSA()
    TSA.analyze_hashtag("%23Ferguson%20%3A(")
