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

    print testfeats.get_

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


def document_features(document):
    return dict([('contains-word(%s)' % w, True) for w in document])


def classify_tweets(classifier, tweet_objects, word_features):

    tweets = [simpleTokenize(tweet.text) for tweet in tweet_objects]
    # feat_set = []
    # for tokens in tweets:
    #     feats = {}
    #     feat_tuple = ()
    #     for token in tokens:
    #         feats[token] = True
    #     feat_tuple = (feats, )
    #     feat_set.append(feat_tuple)

    # negfeats = [(word_feats(movie_reviews.words(fileids=[f])), 'neg') for f in negids]
    feat_set = [word_feats(tokens) for tokens in tweets]
    # feat_set = [((word_feats(tokens)), 'what') for tokens in tweets]

    # feat_set = [dict(token=True) for tokens in tweets for token in tokens]
    # feat_set = [dict(tokens=tokens) for tokens in tweets]
    # feat_set = [(tweet_features(tokens, word_features)) for tokens in tweets]

    # print feat_set[0:2]

    # featuresets = [(document_features(d), d['category']) for d in documents]

    for pdist in classifier.prob_classify_many(feat_set):
        print('%.4f %.4f' % (pdist.prob(classifier.labels()[0]), pdist.prob(classifier.labels()[1])))

    return feat_set


def test_test(classifier):
    lols = ({u'all': True, u'right': True, u'http://t.co/BG3sEog9cl': True, u'am': True, u'To': True, u'Sorry': True, u'#Ferguson': True, u'Happy': True, u'RT': True, u'no': True, u're': True, u'tweets': True, u':': True, u'http': True, u'Thanksgiving': True, u'now': True, u'by': True, u'--': True, u'consumed': True, u'\u2026': True, u'@ExposingALEC': True, u':))': True, u'ALEC': True}, {u'RT': True, u'and': True, u'#Ferguson': True, u':)': True, u'@Op_Israel': True, u'heartwarming': True, u'is': True, u'#Palestine': True, u'so': True, u'between': True, u':': True, u'Solidarity': True})
    # lol = ({'cute': True, 'all': True, 'think': True, 'letterman': True, 'just': True, 'moments': True, 'when': True, 'move': True, 'effects': True, 'enjoyable': True, 'reclaim': True, 'executed': True, 'feat': True, 'its': True, 'before': True, 'note': True, 'style': True, 'death': True, 'buddy': True, 'everything': True, 'reluctant': True, '(': True, 'had': True, ',': True, 'send': True, 'actually': True, 'better': True, 'to': True, 'must': True, 'wags': True, 'win': True, 'save': True, 'norm': True, '?': True, 'then': True, 'his': True, 'prowess': True, 'very': True, 'big': True, 'possibly': True, 'game': True, 'cannot': True, 'courtroom': True, 'they': True, 'formula': True, 'not': True, 'gloom': True, 'school': True, 'gets': True, 'name': True, '--': True, 'follows': True, 'clad': True, 'yeah': True, 'michael': True, 'make': True, 'clown': True, 'father': True, 'true': True, 'stupid': True, 'rockets': True, 't': True, 'shots': True, 'team': True, 'where': True, 'heavy': True, 'lie': True, 'quicker': True, 'old': True, 'picture': True, 'splish': True, 'idea': True, 'ends': True, 'see': True, 'are': True, 'sight': True, 'mine': True, 'absurdity': True, 'special': True, 'out': True, 'even': True, 'comeuppance': True, 'plays': True, 'both': True, "'": True, 'solemn': True, 'movie': True, 'while': True, 'current': True, 're': True, 'connection': True, 'sneakers': True, 'new': True, 'slapstick': True, 'approach': True, 'disney': True, 'be': True, 'we': True, 'were': True, 'here': True, 'quite': True, 'credits': True, 'pooch': True, 'basketball': True, 'sink': True, 'although': True, 'alone': True, 'musical': True, 'predictability': True, 'retriever': True, 'boy': True, 'pairs': True, 'actual': True, 'anything': True, 'of': True, 'could': True, 'or': True, 'david': True, 'motion': True, 'accomplished': True, 'chain': True, 'asked': True, 'jersey': True, 'golden': True, 'own': True, 'family': True, 'josh': True, 'abusive': True, 'mopey': True, 'washington': True, 'number': True, 'whatever': True, 'one': True, 'appropriate': True, 'esteem': True, 'sequences': True, 'owner': True, 'fernwell': True, 'story': True, '"': True, 'from': True, 'i': True, 'would': True, 'paint': True, 'there': True, 'two': True, 'been': True, '.': True, 'zegers': True, 'their': True, 'splash': True, 'newspapers': True, 'recent': True, 'climax': True, 'opens': True, 'more': True, 'back': True, 'snively': True, 'himself': True, 'on': True, 'successful': True, 'but': True, 'surprisingly': True, 'visual': True, 'last': True, 'trying': True, 'with': True, 'than': True, 'bud': True, 'he': True, 'fades': True, 'hire': True, ':': True, 'places': True, 'this': True, 'yeller': True, 'straight': True, 'insists': True, 'up': True, 'air': True, 'trick': True, 'matter': True, 'mascot': True, 'can': True, 'joke': True, 'spilled': True, 'cans': True, 'and': True, 'escapes': True, 'is': True, 'cleaned': True, 'it': True, 'doesn': True, 'an': True, 'twist': True, 'player': True, 'as': True, 'proves': True, 'exist': True, 'at': True, 'have': True, 'in': True, 'faux': True, 'seem': True, 'saw': True, 'tells': True, 'kevin': True, 'if': True, '!': True, 'funny': True, 'court': True, 'no': True, ')': True, 'granted': True, 'cope': True, '-': True, 's': True, 'occasional': True, 'contracts': True, 'that': True, 'interested': True, 'animal': True, 'tricks': True, 'k9': True, 'comedy': True, 'events': True, 'surfaces': True, 'begin': True, 'used': True, 'okay': True, 'marches': True, 'forced': True, 'may': True, 'moment': True, 'buried': True, 'end': True, 'friend': True, 'else': True, 'segment': True, 'finals': True, 'off': True, 'kid': True, 'a': True, 'realized': True, 'least': True, 'for': True, 'montage': True, 'light': True, 'calculated': True, 'well': True, 'dog': True, 'face': True, 'tale': True, 'pet': True, 'cheer': True, 'block': True, 'jeter': True, 'rabies': True, 'the': True, 'self': True, 'once': True})

    return classifier.prob_classify_many(lols)
    # for pdist in
    #     print('%.4f %.4f' % (pdist.prob(classifier.labels()[0], pdist.prob(classifier.labels()[1]))))
