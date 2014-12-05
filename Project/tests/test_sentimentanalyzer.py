import sys
sys.path.insert(0, '../')
from twokenize import simpleTokenize
import tweetfetcher
from nose.tools import with_setup
import sentimentanalyzer as sa

SA = None
fetcher = None


def setup_func():
    global SA, fetcher
    SA = sa.SentimentAnalyzer()
    fetcher = tweetfetcher.TweetFetcher()


@with_setup(setup=setup_func)
def test_read_tweets_from_file():
    global SA
    ts = sa.read_tweets_from_file("Project/traindata/postweets.txt")
    assert(len(ts) == 10000)


@with_setup(setup=setup_func)
def test_filter_tokens():
    global SA
    ts = sa.read_tweets_from_file("Project/traindata/postweets.txt")
    ttokens = [simpleTokenize(t) for t in ts]
    f_tokens = [sa.filter_tokens(tokens) for tokens in ttokens]
    assert(f_tokens is not None)


@with_setup(setup=setup_func)
def test_is_trained():
    global SA
    is_trained = SA.is_trained()
    assert(is_trained is not None)


@with_setup(setup=setup_func)
def test_feature_extraction():
    global SA
    ts = sa.read_tweets_from_file("Project/traindata/postweets.txt")
    ttokens = [simpleTokenize(t) for t in ts]
    f_tokens = [sa.filter_tokens(tokens) for tokens in ttokens]

    ef = [SA.feature_extraction(token_set) for token_set in f_tokens]
    assert(ef is not None)


@with_setup(setup=setup_func)
def test_feature_extraction_movie_reviews():
    assert(True)


@with_setup(setup=setup_func)
def test_train_with_movie_db():
    assert(True)


@with_setup(setup=setup_func)
def test_load_classifier():
    global SA
    SA.classifier = None
    SA.load_classifier()
    assert(SA.classifier is not None)



@with_setup(setup=setup_func)
def test_train():
    global SA
    SA.classifier = None
    SA.train()
    assert(SA.classifier is not None)



@with_setup(setup=setup_func)
def test_classify():
    global SA, fetcher
    tweets = fetcher.get_tweets("%23twitter")
    analyzed_tweets = SA.classify(tweets)
    for t in analyzed_tweets:
        assert(t.polarity is not None)
