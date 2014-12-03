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

class User(object):
    def __init__(self, json_object):
        self.__dict__ = json_object


class Tweet(object):
    def __init__(self, json_object):
        self.__dict__ = json_object
        self.user = User(self.user)


class AnalyzedTag(object):

    tweet = None
    hashtags = []
    date = None
    polarity = None
    pdist = None

    def __init__(self, tweet, pdist):
        self.hashtags = [tag['text'] for tag in tweet.entities['hashtags']]
        self.pdist = pdist


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
