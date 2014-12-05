from nltk.classify import NaiveBayesClassifier, util, accuracy
from nltk import FreqDist
from nltk.corpus import movie_reviews
from twokenize import simpleTokenize
import random
from debug import DLOG
import datetime
import cPickle


##### HELPER METHODS ######
def read_tweets_from_file(filename):
    """
    Helper method for reading training tweets from file.
    """
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


def filter_tokens(tokens):
    """
    Helper method.
    Token filtering method.
    List of tokens given as input, filtered list returned.
    """
    filtered_tokens = list(tokens)
    for token in tokens:
        if (token.find("http") > -1):
            filtered_tokens.remove(token)
            # DLOG("delete" + token)
        elif (token.find("RT") > -1):
            filtered_tokens.remove(token)
            # DLOG("delete" + token)
        elif (token.find("@") > -1):
            filtered_tokens.remove(token)
            # DLOG("delete" + token)
        elif (token.find("#") > -1):
            filtered_tokens.remove(token)
            # DLOG("delete" + token)
        elif token.find("www") > -1:
            filtered_tokens.remove(token)
            # DLOG("delete" + token)

    return filtered_tokens



class SentimentAnalyzer(object):
    """
    SentimentAnalyzer class for analyzing tweets

    """

    classifier = None
    sentiment_features = None
    use_movie_reviews = False

    def __init__(self):
        super(SentimentAnalyzer, self).__init__()


    def is_trained(self):
        """
        Helper method for classify
        """
        return True if self.classifier is not None else False


    def feature_extraction(self, tweet):
        """
        Extraction of features.
        Tweets given as input
        Dictionary with features returned
        """
        tweet_words = set(tweet)
        features = {}
        for word in self.sentiment_features:
            features['contains(%s)' % word] = (word in tweet_words)
        return features


    def feature_extraction_movie_reviews(self, tweet):
        """
        Features for training with movie reviews
        - this does not yield particularly good results
        """
        return dict([(word, True) for word in tweet])


    def train_with_movie_db(self):
        """
        Training possible with movie reviews
        - this does not yield particularly good results
        """
        self.use_movie_reviews = True

        negids = movie_reviews.fileids('neg')
        posids = movie_reviews.fileids('pos')

        negfeats = [(self.feature_extraction_movie_reviews(movie_reviews.words(fileids=[f])),
                     "negative") for f in negids]
        posfeats = [(self.feature_extraction_movie_reviews(movie_reviews.words(fileids=[f])),
                     "positive") for f in posids]

        negcutoff = len(negfeats) * 3 / 4
        poscutoff = len(posfeats) * 3 / 4

        trainfeats = negfeats[:negcutoff] + posfeats[:poscutoff]
        testfeats = negfeats[negcutoff:] + posfeats[poscutoff:]

        DLOG("train on %d instances, test on %d instances" % (len(trainfeats), len(testfeats)))

        self.classifier = NaiveBayesClassifier.train(trainfeats)

        DLOG("accuracy: " + str(util.accuracy(self.classifier, testfeats)))
        DLOG(self.classifier.show_most_informative_features())



    def load_classifier(self):
        """
        Load classifier from file.
        Given classifier is hardcoded at the time being.
        """
        time_stamp = "2014-12-03 16:15:10"
        with open("tweetfeatures/tweet_features_" + time_stamp + ".pkl", 'rb') as fid:
            self.sentiment_features = cPickle.load(fid)

        with open("classifier/classifier_" + time_stamp + ".pkl", 'rb') as fid:
            self.classifier = cPickle.load(fid)


    def train(self, arg):
        """
        Trains the classifier with saved train data
        Sentiment features and classifier are stored in class variables,
        and also dumped with cPickle
        """
        pos_tweets = read_tweets_from_file("traindata/postweets.txt")
        neg_tweets = read_tweets_from_file("traindata/negtweets.txt")
        objective_tweets1 = read_tweets_from_file("traindata/objectivetweets.txt")
        objective_tweets2 = read_tweets_from_file("traindata/objectivetweets2.txt")
        objective_tweets3 = read_tweets_from_file("traindata/objectivetweets3.txt")
        objective_tweets = objective_tweets1 + objective_tweets2 + objective_tweets3
        random.shuffle(objective_tweets)

        # pos_tweets2 = read_tweets_from_file("traindata/happytweets.txt")
        # pos_tweets.extend(pos_tweets2)
        # neg_tweets2 = read_tweets_from_file("traindata/sadtweets.txt")
        # neg_tweets.extend(neg_tweets2)

        training_tweet_number = 3000
        if arg is not None:
            if arg > 0 & arg < 10000:
                training_tweet_number = arg


        pos_tokens = [simpleTokenize(tweet) for tweet in pos_tweets[:training_tweet_number]]
        neg_tokens = [simpleTokenize(tweet) for tweet in neg_tweets[:training_tweet_number]]
        objective_tokens = [simpleTokenize(tweet) for tweet in objective_tweets[:training_tweet_number]]

        pos_filtered_tokens = [filter_tokens(tokens) for tokens in pos_tokens]
        neg_filtered_tokens = [filter_tokens(tokens) for tokens in neg_tokens]
        objective_filtered_tokens = [filter_tokens(tokens) for tokens in objective_tokens]


        pos_tweet_tokens = [dict(tokens=tokens, polarity="positive") for tokens in pos_filtered_tokens]
        neg_tweet_tokens = [dict(tokens=tokens, polarity="negative") for tokens in neg_filtered_tokens]
        objective_tweet_tokens = [dict(tokens=tokens, polarity="objective") for tokens in objective_filtered_tokens]
        all_tokens = pos_tweet_tokens + neg_tweet_tokens + objective_tweet_tokens


        all_words = FreqDist(t.lower() for d in all_tokens for t in d["tokens"])
        self.sentiment_features = all_words.keys()

        time_stamp = str(datetime.datetime.now())[:19]
        feature_file = "tweetfeatures/tweet_features_" + time_stamp + ".pkl"
        with open(feature_file, "wb") as fid:
            cPickle.dump(self.sentiment_features, fid)

        random.shuffle(all_tokens)

        # feature extraction
        featuresets = [(self.feature_extraction(d["tokens"]), d["polarity"]) for d in all_tokens]

        feature_length = len(featuresets)

        train_set, test_set = featuresets[:int(feature_length * 0.8)], featuresets[int(feature_length * 0.8):]

        self.classifier = NaiveBayesClassifier.train(train_set)

        DLOG(accuracy(self.classifier, test_set))
        self.classifier.show_most_informative_features()

        classifier_file = "classifier/classifier_" + time_stamp + ".pkl"
        with open(classifier_file, "wb") as fid:
            cPickle.dump(self.classifier, fid)
        # return classifier


    def classify(self, tweets):
        """
        Classify tweets
        Tweets given as input
        Tweets returned with polarity indicating positive or negative sentiment
        """
        if not self.is_trained():
            DLOG("Training is needed. Loading classifier from disk.")

            # INFORM TO USER THAT TRAINING IS NEED AND CAN TAKE SOME TIME
            self.load_classifier()
            self.classify(tweets)

        else:
            tokens = [simpleTokenize(tweet.text) for tweet in tweets]

            filtered_tokens = [filter_tokens(token_set) for token_set in tokens]


            extraction_start = datetime.datetime.now()  # request timing
            DLOG("Start feature extraction")
            feature_sets = None
            if self.use_movie_reviews:
                feature_sets = [self.feature_extraction_movie_reviews(token_set) for token_set in filtered_tokens]
            else:
                feature_sets = [self.feature_extraction(token_set) for token_set in filtered_tokens]
            DLOG("Feature extraction time: " + str(datetime.datetime.now() - extraction_start))  # request timing


            classification_start = datetime.datetime.now()  # request timing
            DLOG("Start classification")
            prob_dists = []

            for feature_set in feature_sets:
                prob_dists.append(self.classifier.prob_classify(feature_set))


            DLOG("Classification time: " + str(datetime.datetime.now() - classification_start))  # request timing

            [tweet.set_polarity(prob_dists[tweets.index(tweet)]) for tweet in tweets]
            return tweets
