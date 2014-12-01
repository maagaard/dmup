import nltk.classify.util
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import movie_reviews
# from re import split
import twitter
import happyfuntokenizing
from twokenize import simpleTokenize
import nltk
import random

# Training on movie_reviews
# train on twitter data as well?

# TOKENIZER = "HAPPYFUN"
TOKENIZER = "ARK"
OFFLINE = False


def word_feats(words):
    return dict([(word, True) for word in words])


def film_review_features():
    negids = movie_reviews.fileids('neg')
    posids = movie_reviews.fileids('pos')

    negfeats = [(word_feats(movie_reviews.words(fileids=[f])), 'neg') for f in negids]
    posfeats = [(word_feats(movie_reviews.words(fileids=[f])), 'pos') for f in posids]

    negcutoff = len(negfeats) * 3 / 4
    poscutoff = len(posfeats) * 3 / 4

    trainfeats = negfeats[:negcutoff] + posfeats[:poscutoff]
    testfeats = negfeats[negcutoff:] + posfeats[poscutoff:]
    print 'train on %d instances, test on %d instances' % (len(trainfeats), len(testfeats))

    classifier = NaiveBayesClassifier.train(trainfeats)

    print 'accuracy:', nltk.classify.util.accuracy(classifier, testfeats)
    classifier.show_most_informative_features()


def extract_features(feature_data):

    return



# --- Word split method
# pos_tweets = tweets["pos"]
# neg_tweets = tweets["neg"]
# pos_words = [split('\W+', tweet.text) for tweet in pos_tweets]
# neg_words = [split('\W+', tweet.text) for tweet in neg_tweets]
# tweets = pos_words + neg_words
# # -
# pos_test_tweets = test_tweets["pos"]
# neg_test_tweets = test_tweets["neg"]
# pos_test_words = [split('\W+', tweet.text) for tweet in pos_test_tweets]
# neg_test_words = [split('\W+', tweet.text) for tweet in neg_test_tweets]
# test_tweets = pos_test_words + neg_test_words

# --- Full tweet method
# pos_tweets = [t.text for t in tweets["pos"]]
# neg_tweets = [t.text for t in tweets["neg"]]
# tweets = pos_tweets + neg_tweets
# # -
# pos_test_tweets = [t.text for t in test_tweets["pos"]]
# neg_test_tweets = [t.text for t in test_tweets["neg"]]
# test_tweets = pos_test_tweets + neg_test_tweets


# # ----
# all_words = nltk.FreqDist(w.lower() for t in tweets for w in t)
# word_features = all_words.keys()    # set a limit so not all words are used. e.g. [:len(self)/2]
# # print len(all_words.keys())

# all_test_words = nltk.FreqDist(w.lower() for t in test_tweets for w in t)
# test_word_features = all_test_words.keys()

def tweet_features(tweet, word_features):
    tweet_words = set(tweet)
    features = {}
    for word in word_features:
        features['contains(%s)' % word] = (word in tweet_words)
    return features


def train():

    if OFFLINE:
        tweets = twitter.get_offline_tweets()
        test_tweets = twitter.get_offline_test_tweets()
    else:
        tweets = twitter.get_training_tweets()
        test_tweets = twitter.get_test_tweets()


    # --- Tokenize method - HappyFunTokenizing
    if TOKENIZER == "HAPPYFUN":
        tokenizer = happyfuntokenizing.Tokenizer(preserve_case=False)
        pos_tweet_tokens = [dict(tokens=tokenizer.tokenize(tweet.text),
                            polarity="positive") for tweet in tweets["pos"]]
        neg_tweet_tokens = [dict(tokens=tokenizer.tokenize(tweet.text),
                            polarity="negative") for tweet in tweets["neg"]]
        tweets = pos_tweet_tokens + neg_tweet_tokens
        # print pos_tweet_tokens
        # -
        pos_test_tweet_tokens = [dict(tokens=tokenizer.tokenize(tweet.text),
                                      polarity="positive") for tweet in test_tweets["pos"]]
        neg_test_tweet_tokens = [dict(tokens=tokenizer.tokenize(tweet.text),
                                      polarity="negative") for tweet in test_tweets["neg"]]
        test_tweets = pos_test_tweet_tokens + neg_test_tweet_tokens

    else:
        pos_tweet_tokens = [dict(tokens=simpleTokenize(tweet.text), polarity="positive") for tweet in tweets["pos"]]
        neg_tweet_tokens = [dict(tokens=simpleTokenize(tweet.text), polarity="negative") for tweet in tweets["neg"]]
        tweets = pos_tweet_tokens + neg_tweet_tokens
        # print pos_tweet_tokens
        # -
        pos_test_tweet_tokens = [dict(tokens=simpleTokenize(tweet.text),
                                      polarity="positive") for tweet in test_tweets["pos"]]
        neg_test_tweet_tokens = [dict(tokens=simpleTokenize(tweet.text),
                                      polarity="negative") for tweet in test_tweets["neg"]]
        test_tweets = pos_test_tweet_tokens + neg_test_tweet_tokens


    # test_tweet_tokens = [tokenizer.tokenize(tweet.text) for tweet in (test_tweets["pos"] + test_tweets["neg"])]


    all_words = nltk.FreqDist(t.lower() for d in tweets for t in d["tokens"])
    word_features = all_words.keys()

    random.shuffle(tweets)
    random.shuffle(test_tweets)


    train_set = [(tweet_features(d["tokens"], word_features), d["polarity"]) for d in tweets]
    test_set = [(tweet_features(d["tokens"], word_features), d["polarity"]) for d in test_tweets]


    classifier = nltk.NaiveBayesClassifier.train(train_set)

    # print classifier.classify(document_features(documents[53]))
    # print documents[53]['text'][:60]

    print nltk.classify.accuracy(classifier, test_set)
    classifier.show_most_informative_features()

    return classifier, word_features


def featstuff(tokens):
        tweet_tokens = set(tokens)
        features = {}
        for word in tweet_tokens:
            features['contains(%s)' % word] = (word in tweet_tokens)
        return features


def classify_tweets(classifier, tweet_objects, word_features):

    tweets = [simpleTokenize(tweet.text) for tweet in tweet_objects]

    feat_set = [(tweet_features(tokens, word_features), "pol") for tokens in tweets]


    # featuresets = [(document_features(d), d['category']) for d in documents]

    for pdist in classifier.prob_classify(feat_set):
        print('%.4f %.4f' % (pdist.prob(classifier.labels()[0], pdist.prob(classifier.labels()[1]))))
