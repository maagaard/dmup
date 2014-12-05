import sys
sys.path.insert(0, '../')
import tsa
import tweetfetcher
from nose.tools import with_setup
import sentimentanalyzer as sa

SA = None


def setup_func():
    global SA
    SA = sa.SentimentAnalyzer()


@with_setup(setup=setup_func)
def test_sort():


@with_setup(setup=setup_func)
def test_read_tweets_from_file():


@with_setup(setup=setup_func)
def test_filter_tokens():



@with_setup(setup=setup_func)
def test_is_trained():



@with_setup(setup=setup_func)
def test_feature_extraction_movie_reviews():
    assert(True)


@with_setup(setup=setup_func)
def test_train_with_movie_db():



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

