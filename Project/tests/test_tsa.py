import sys
sys.path.insert(0, '../')
import tsa
import tweetfetcher


def test_sort():

    fetcher = tweetfetcher.TweetFetcher()
    tweets = fetcher.get_tweets("%23Ferguson")

    sorted_tweets = tsa.sort_tweets(tweets)

    for i in xrange(1, len(sorted_tweets) - 1):
        assert(sorted_tweets[i - 1].get_date() <= sorted_tweets[i].get_date())



def test_tsa():
    TSA = tsa.TSA()

    do_stuff = TSA.analyze_hashtag()

    print do_stuff











if __name__ == '__main__':
    test_sort()
