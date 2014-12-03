#!/usr/bin/env python
# encoding: utf-8
import json


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
    def __init__(self, something):
        self.__dict__ = something
        self.

    