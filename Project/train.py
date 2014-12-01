import nltk.classify.util
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import movie_reviews
from re import split
import twitter
import model

# Training on movie_reviews
# train on twitter data as well?


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



print "My testing"


# tweets = twitter.get_training_tweets()
tweets = twitter.get_offline_tweets()


pos_tweets = tweets["pos"]
neg_tweets = tweets["neg"]


pos_words = [split('\W+', tweet.text) for tweet in pos_tweets]
neg_words = [split('\W+', tweet.text) for tweet in neg_tweets]
documents = pos_words + neg_words

# for n in range(len(documents)):
#   html = message_from_string(documents[n]['email']).get_payload()
#   while not isinstance(html, str):                 # Multipart problem
#     html = html[0].get_payload()
#   text = ' '.join(BS(html).findAll(text=True))      # Strip HTML
#   documents[n]['html'] = html
#   documents[n]['text'] = text
#   documents[n]['words'] = split('\W+', text)        # Find words

all_words = nltk.FreqDist(w.lower() for d in documents for w in d)

# word_features = all_words.keys()[:2000]
print len(all_words.keys())

# def document_features(document):
#   document_words = set(document['words'])
#   features = {}
#   for word in word_features:
#     features['contains(%s)' % word] = (word in document_words)
#   return features


# import random
# random.shuffle(documents)

# featuresets = [(document_features(d), d['category']) for d in documents]
# train_set, test_set = featuresets[721:], featuresets[:721]

# classifier = nltk.NaiveBayesClassifier.train(train_set)

# # print classifier.classify(document_features(documents[53]))
# # print documents[53]['text'][:60]
# print nltk.classify.accuracy(classifier, test_set)
