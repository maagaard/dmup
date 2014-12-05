#!/usr/bin/env python
# encoding: utf-8
# import json


# class Tweet(object):
#   text = str
#   date = str
#   language = str
#   favorite_count = int
#   retweet_count = int
#   user_location = str


#   """docstring for Tweet"""
#   def __init__(self, json):
#       # super(Tweet, self).__init__()
#       # self.text = text
#       self.text = json

#   @property
#   def has_text(self):
#       return self.text != ""

#   # @text.setter
#   # def text(self, text):
#   #   self.text = text

from dateutil.parser import parse


class User(object):
    def __init__(self, json_object):
        self.__dict__ = json_object


class Tweet(object):
    pdist = None
    polarity = None

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
        obj = self.pdist["objective"]
    # print "Positive: " + str(pos) + ", negative: " + str(neg) + ", objective: " + str(self.pdist.prob("objective"))
        # print("positve: %.2f, negative: %.2f, objective: %.2f" % (round(pos, 2),
        #                                                           round(neg, 2),
        #                                                           round(obj, 2)))

        self.polarity = round(round(pos, 2) - round(neg, 2), 2)
        return self.polarity


class AnalyzedTag(object):

    tweet = None
    hashtags = []
    date = None
    polarity = None
    pdist = None

    def __init__(self, tweet, pdist):
        self.hashtags = [tag['text'] for tag in tweet.entities['hashtags']]
        self.pdist = pdist
        self.tweet = tweet
        self.polarity = self.calculate_polarity()


    def get_polarity(self):
        if self.polarity is None:
            self.polarity = self.calculate_polarity()
        return self.polarity


    def calculate_polarity(self):
        pos = self.pdist.prob("positive")
        neg = self.pdist.prob("negative")
        obj = self.pdist.prob("objective")

    # print "Positive: " + str(pos) + ", negative: " + str(neg) + ", objective: " + str(self.pdist.prob("objective"))

        # print("positve: %.2f, negative: %.2f, objective: %.2f" % (round(pos, 2),
        #                                                           round(neg, 2),
        #                                                           round(obj, 2)))

        polarity = round(round(pos, 2) - round(neg, 2), 2)
        return polarity
