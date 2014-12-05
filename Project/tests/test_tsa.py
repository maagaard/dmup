import sys
sys.path.insert(0, '../')
import tsa
import tweetfetcher
from nose.tools import with_setup

fetcher = None
TSA = None


def setup_func():
    global fetcher, TSA
    fetcher = tweetfetcher.TweetFetcher()
    TSA = tsa.TSA()


@with_setup(setup=setup_func)
def test_sort():
    global fetcher
    tweets = fetcher.get_tweets("%23Twitter")
    sorted_tweets = tsa.sort_tweets(tweets)

    for i in xrange(1, len(sorted_tweets) - 1):
        assert(sorted_tweets[i - 1].get_date() <= sorted_tweets[i].get_date())


@with_setup(setup=setup_func)
def test_set_output_mode():
    global TSA
    TSA.set_output_mode("weeks")
    assert(TSA.output_mode == "weeks")
    TSA.set_output_mode(1)
    assert(TSA.output_mode == "days")
    TSA.set_output_mode("somethingelse")
    assert(TSA.output_mode == "hours")


@with_setup(setup=setup_func)
def test_analyze_hashtag():
    global TSA
    tweets = TSA.analyze_hashtag("%23twitter", 100)
    for t in tweets:
        assert(t.polarity is not None)


@with_setup(setup=setup_func)
def test_output_tweets():
    global TSA
    TSA.analyze_hashtag("%23twitter", 100)
    tweets = TSA.output_tweets()
    assert(tweets is not None)
