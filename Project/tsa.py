__author__ = "Emil Maagaard & Bjarke Vad Andersen"
__credits__ = []
__version__ = "1.0"

from sentimentanalyzer import SentimentAnalyzer
from tweetfetcher import TweetFetcher
from debug import DLOG
import datetime


def sort_tweets(tweets):
    """
    Helper method for sorting tweets in chronological order.
    """
    tweets.sort(key=lambda x: x.get_date())
    return tweets


class TSA(object):
    """
    TwitterSentimentAnalyzer
    Class for sentiment analyzing tweets.
    """

    sa = SentimentAnalyzer()
    tweet_fetcher = TweetFetcher()

    output_modes = ["hours", "days", "weeks"]
    output_mode = output_modes[0]

    analyzed_tweets = None
    output_bins = None


    def __init__(self):
        super(TSA, self).__init__()
        self.sa.load_classifier()
        # self.tweet_fetcher = TweetFetcher()


    def set_output_mode(self, mode="hours"):
        """
        Sets the preffered bin size for output.
        input "mode" can be any of "hours", "days", "weeks", 0, 1 or 2.
        """
        if (mode == "hours") | (mode == "days") | (mode == "weeks"):
            self.output_mode = mode
        else:
            try:
                self.output_mode = self.output_modes[mode]
            except Exception, e:
                DLOG("Output mode not set correctly: " + str(e))
                self.output_mode = "hours"


    def analyze_hashtag(self, hashtag, count=200):
        """
        Analyze a hashtag given as input.
        Amount of tweets are 200 be default, but can be given as argument also.
        Returns analyzed tweets in a list.
        """
        tweets = []

        for x in xrange(0, int(count / 100)):
            tweets.extend(self.tweet_fetcher.get_tweets(hashtag))

        analyzed_tweets = sort_tweets(self.sa.classify(tweets))

        self.analyzed_tweets = analyzed_tweets

        return analyzed_tweets


    def set_analyzed_tweets(self, tweets):
        """
        Set analyzed tweets sorted. E.g. from saved analyzed tweets.
        """
        self.analyzed_tweets = sort_tweets(tweets)


    def output_tweets(self):
        """
        Outputs analyzed tweets in bins.
        Bin size (hours, days or weeks) determined by self.output_mode
        """
        if self.analyzed_tweets is None:
            return None

        splitter = 0
        if (self.output_mode == "days"):
            splitter = 86400  # 1 day in seconds
            pass
        elif (self.output_mode == "weeks"):
            splitter = 604800  # 1 week in seconds
            pass
        else:
            splitter = 3600  # 1 hours in seconds
            pass

        sorted_tweets = sort_tweets(self.analyzed_tweets)
        self.analyzed_tweets = sorted_tweets

        oldest = self.analyzed_tweets[0].get_date()
        newest = self.analyzed_tweets[-1].get_date()

        delta = int(((newest - oldest).total_seconds()) / splitter)

        bins = []
        hour_bin = []
        for x in xrange(1, delta + 2):
            upper_limit = oldest + datetime.timedelta(seconds=splitter * x)
            lower_limit = upper_limit - datetime.timedelta(seconds=splitter)

            hour_bin = []
            for tweet in self.analyzed_tweets:
                if tweet.get_date() > upper_limit:
                    bins.append(hour_bin)
                    DLOG("Bin containing " + str(len(hour_bin)) + " tweets")
                    break
                elif tweet.get_date() < lower_limit:
                    continue
                else:
                    hour_bin.append(tweet)

        DLOG("Bin containing " + str(len(hour_bin)) + " tweets")
        bins.append(hour_bin)

        self.output_bins = bins

        return bins
        #### Alternate binning ####
        # if len(analyzed_tweets) < 500:
        #     bin_size = 10
        # else:
        #     bin_size = int(len(analyzed_tweets) * .02)
        # bins = []
        # for count in range(0, int(len(analyzed_tweets) / bin_size)):
        #     pol_bin = [tweet.polarity for tweet in analyzed_tweets[(count * bin_size):((count + 1) * bin_size)]]
        #     bins.append(pol_bin)
        # DLOG([sum(bin) for bin in bins])


if __name__ == '__main__':
    TSA = TSA()
    TSA.analyze_hashtag("%23Ferguson%20%3A(")
