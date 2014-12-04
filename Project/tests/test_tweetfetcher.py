import sys
sys.path.insert(0, '../')
import tweetfetcher


def test():
    """docstring"""



    pass





def test_tweetfetcher():
    fetcher = tweetfetcher.TweetFetcher()
    tweets = fetcher.get_tweets("%23twitter")
    assert len(tweets) == 100




def run_all_tests():
    test()
    test_tweetfetcher()


if __name__ == '__main__':
    run_all_tests()
