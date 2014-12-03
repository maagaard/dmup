

from sentimentanalyzer import SentimentAnalyzer
from tweetfetcher import TweetFetcher

fetcher = TweetFetcher()
tweets = fetcher.get_tweets("%23Ferguson")

sa = SentimentAnalyzer()
sa.load_classifier()

ats = sa.classify(tweets)

print ats[0]
print ats[0].hashtags
print ats[0].get_polarity()
