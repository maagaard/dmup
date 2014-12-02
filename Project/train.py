import nltk.classify.util
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import movie_reviews
# from re import split
import twitter
import happyfuntokenizing
from twokenize import simpleTokenize
import nltk
import random
from debug import DLOG

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

    print testfeats.get_

    classifier = NaiveBayesClassifier.train(trainfeats)

    print 'accuracy:', nltk.classify.util.accuracy(classifier, testfeats)
    classifier.show_most_informative_features()




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


def document_features(document):
    return dict([('contains-word(%s)' % w, True) for w in document])


def extract_features(tweets):
    tweets = tweets




def classify_tweets(classifier, tweets, word_features):

    tokens = [simpleTokenize(tweet.text) for tweet in tweets]

    filtered_tokens = [filter_tokens(token_set) for token_set in tokens]

    # feat_set = []
    # for tokens in tweets:
    #     feats = {}
    #     feat_tuple = ()
    #     for token in tokens:
    #         feats[token] = True
    #     feat_tuple = (feats, )
    #     feat_set.append(feat_tuple)

    # print tweets[0:2]

    # negfeats = [(word_feats(movie_reviews.words(fileids=[f])), 'neg') for f in negids]

    # feat_set = [word_feats(tokens) for tokens in tweets]

    # feat_set = [((word_feats(tokens)), 'what') for tokens in tweets]

    feature_sets = [tweet_features(token_set, word_features) for token_set in filtered_tokens]

    # feat_set = [dict(token=True) for tokens in tweets for token in tokens]
    # feat_set = [dict(tokens=tokens) for tokens in tweets]
    # feat_set = [(tweet_features(tokens, word_features)) for tokens in tweets]

    # print feat_set[0:2]

    # featuresets = [(document_features(d), d['category']) for d in documents]

    for pdist in classifier.prob_classify_many(feature_sets):
        print('%.4f %.4f' % (pdist.prob(classifier.labels()[0]), pdist.prob(classifier.labels()[1])))

    return pdist



def test_test(classifier):
    lols = (
            {u'all': True, u'right': True, u'http://t.co/BG3sEog9cl': True, u'am': True, u'To': True, u'Sorry': True,
             u'#Ferguson': True, u'Happy': True, u'RT': True, u'no': True, u're': True, u'tweets': True, u':': True,
             u'http': True, u'Thanksgiving': True, u'now': True, u'by': True, u'--': True, u'consumed': True,
             u'\u2026': True, u'@ExposingALEC': True, u':))': True, u'ALEC': True},
            {u'RT': True, u'and': True,
             u'#Ferguson': True, u':)': True, u'@Op_Israel': True, u'heartwarming': True, u'is': True,
             u'#Palestine': True, u'so': True, u'between': True, u':': True, u'Solidarity': True})

    return classifier.prob_classify_many(lols)
    # for pdist in
    #     print('%.4f %.4f' % (pdist.prob(classifier.labels()[0], pdist.prob(classifier.labels()[1]))))



def test_filter():
    lol = [
            [u'Well', u'shut', u'my', u'mouth', u'...', u':)', u'Meet', u'#Devonte', u',', u'the', u'little', u'boy',
             u'with', u'a', u'big', u'heart', u'-', u'Paper', u'Trail', u'#ferguson', u'#freehugs',
             u'http://t.co/Fd6GEpI73D'],
            [u'RT', u'@Nettaaaaaaaa', u':', u'I', u'love', u'this', u'!', u'Some', u'@STLouisRams', u'players',
             u'come', u'out', u'with', u'their', u'HANDS', u'UP', u'for', u'#Ferguson', u'https://t.co/36D4h14p5S',
             u':)', u'great', u'shot', u'@', u'\u2026']]

    print "Testing tweet filtering:"
    print lol
    print "Number of tokens: " + str(len(lol[0]))
    print "---------"
    filtered_tokens = [filter_tokens(tokens) for tokens in lol]
    print filtered_tokens
    print "Number of tokens: " + str(len(filtered_tokens[0]))


def filter_tokens(tokens):
    # for tokens in token_list:
    filtered_tokens = list(tokens)
    for token in tokens:
        if (token.find("http") > -1):
            filtered_tokens.remove(token)
            DLOG("delete" + token)
        elif (token.find("RT") > -1):
            filtered_tokens.remove(token)
            DLOG("delete" + token)
        elif (token.find("@") > -1):
            filtered_tokens.remove(token)
            DLOG("delete" + token)
        elif (token.find("#") > -1):
            filtered_tokens.remove(token)
            DLOG("delete" + token)
        elif token.find("www") > -1:
            filtered_tokens.remove(token)
            DLOG("delete" + token)

    return filtered_tokens


def read_tweets_from_file(filename):
    tweets = []
    with open(filename, 'r') as data_file:
        text = ""
        for line in data_file:
            if line != "-- \n":
                text += line
            else:
                tweets.append(text.replace("\n", " "))
                text = ""

    return tweets


def training():

    pos_tweets = read_tweets_from_file("postweets.txt")
    neg_tweets = read_tweets_from_file("negtweets.txt")
    objective_tweets1 = read_tweets_from_file("objectivetweets.txt")
    objective_tweets2 = read_tweets_from_file("objectivetweets2.txt")
    objective_tweets3 = read_tweets_from_file("objectivetweets3.txt")
    objective_tweets = objective_tweets1 + objective_tweets2 + objective_tweets3
    random.shuffle(objective_tweets)

    # pos_tweets2 = read_tweets_from_file("happytweets.txt")
    # pos_tweets.extend(pos_tweets2)
    # neg_tweets2 = read_tweets_from_file("sadtweets.txt")
    # neg_tweets.extend(neg_tweets2)

    pos_tokens = [simpleTokenize(tweet) for tweet in pos_tweets[:1000]]
    neg_tokens = [simpleTokenize(tweet) for tweet in neg_tweets[:1000]]
    objective_tokens = [simpleTokenize(tweet) for tweet in objective_tweets[:1000]]

    pos_filtered_tokens = [filter_tokens(tokens) for tokens in pos_tokens]
    neg_filtered_tokens = [filter_tokens(tokens) for tokens in neg_tokens]
    objective_filtered_tokens = [filter_tokens(tokens) for tokens in objective_tokens]

    #######

    pos_tweet_tokens = [dict(tokens=tokens, polarity="positive") for tokens in pos_filtered_tokens]

    neg_tweet_tokens = [dict(tokens=tokens, polarity="negative") for tokens in neg_filtered_tokens]

    objective_tweet_tokens = [dict(tokens=tokens, polarity="objective") for tokens in objective_filtered_tokens]

    all_tokens = pos_tweet_tokens + neg_tweet_tokens + objective_tweet_tokens

    # test_tweet_tokens = [tokenizer.tokenize(tweet.text) for tweet in (test_tweets["pos"] + test_tweets["neg"])]

    all_words = nltk.FreqDist(t.lower() for d in all_tokens for t in d["tokens"])
    word_features = all_words.keys()

    random.shuffle(all_tokens)


# feate extraction?
    featuresets = [(tweet_features(d["tokens"], word_features), d["polarity"]) for d in all_tokens]

    # featuresets = [(document_features(d), d['category']) for d in documents]

    feature_length = len(featuresets)  # len(pos_tweets) + len(neg_tweets)

    train_set, test_set = featuresets[:int(feature_length * 0.8)], featuresets[int(feature_length * 0.8):]

    # happy_set = [(tweet_features(d["tokens"], word_features), d["polarity"]) for d in happy_tokens]

    classifier = nltk.NaiveBayesClassifier.train(train_set)

    # print classifier.classify(document_features(documents[53]))
    # print documents[53]['text'][:60]

    print nltk.classify.accuracy(classifier, test_set)
    classifier.show_most_informative_features()

    return classifier, word_features


def test_dlog():
    DLOG("Print if debug is True")
