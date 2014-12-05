import sys
sys.path.insert(0, '../')
import tweetfetcher
from nose.tools import with_setup

fetcher = None


def setup_func():
    global fetcher
    fetcher = tweetfetcher.TweetFetcher()


@with_setup(setup=setup_func)
def test_get_client_status():
    global fetcher
    assert 0 <= fetcher.get_client_status() <= 450


@with_setup(setup=setup_func)
def test_get_tweets():
    global fetcher
    tweets = fetcher.get_tweets("%23twitter")
    assert len(tweets) == 100


@with_setup(setup=setup_func)
def test_get_tweets_as_json():
    global fetcher
    json = fetcher.get_tweets_as_json("%23twitter")
    assert len(json['statuses']) == 100


@with_setup(setup=setup_func)
def test_stop_fetching():
    global fetcher
    fetcher.stop_fetching()
    assert fetcher.tweet_max_id is None
