__author__ = "Emil Maagaard & Bjarke Vad Andersen"
__credits__ = []
__version__ = "1.0"

from dateutil.parser import parse


class User(object):
    def __init__(self, json_object):
        self.__dict__ = json_object


class Tweet(object):
    pdist = None
    polarity = None
    objectivity = None

    def __init__(self, json_object):
        self.__dict__ = json_object
        if self.user is not None:
            self.user = User(self.user)
        self.hashtags = [tag['text'] for tag in self.entities['hashtags']]


    def get_date(self):
        return parse(self.created_at)
        # self.entities = Entities(self.entities)


    def get_polarity(self):
        return self.polarity


    def set_polarity(self, pdist):
        self.pdist = dict(positive=pdist.prob("positive"),
                          negative=pdist.prob("negative"),
                          objective=pdist.prob("objective"))

        pos = self.pdist["positive"]
        neg = self.pdist["negative"]
        self.objectivity = self.pdist["objective"]
    # print "Positive: " + str(pos) + ", negative: " + str(neg) + ", objective: " + str(self.pdist.prob("objective"))
        # print("positve: %.2f, negative: %.2f, objective: %.2f" % (round(pos, 2),
        #                                                           round(neg, 2),
        #                                                           round(obj, 2)))

        self.polarity = round(round(pos, 2) - round(neg, 2), 2)
        return self.polarity


class SlimTweet(Tweet):
    pdist = None
    polarity = None
    objectivity = None

    def __init__(self, tweet):
        self.text = tweet.text
        self.polarity = tweet.polarity
        self.created_at = tweet.created_at
        self.hashtags = tweet.hashtags
        self.pdist = tweet.pdist


    def get_date(self):
        return parse(self.created_at)
        # self.entities = Entities(self.entities)


    def get_polarity(self):
        return self.polarity


    def set_polarity(self, pdist):
        self.pdist = dict(positive=pdist.prob("positive"),
                          negative=pdist.prob("negative"),
                          objective=pdist.prob("objective"))

        pos = self.pdist["positive"]
        neg = self.pdist["negative"]
        self.objectivity = self.pdist["objective"]
    # print "Positive: " + str(pos) + ", negative: " + str(neg) + ", objective: " + str(self.pdist.prob("objective"))
        # print("positve: %.2f, negative: %.2f, objective: %.2f" % (round(pos, 2),
        #                                                           round(neg, 2),
        #                                                           round(obj, 2)))

        self.polarity = round(round(pos, 2) - round(neg, 2), 2)
        return self.polarity
