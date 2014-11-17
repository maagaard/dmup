


class Sentiment(object):
    """docstring for Sentiment"""

    features = []
    labels = ['negative', 'positive', 'sad', 'excited', 'angry', 'happy', 'bored']

    feature_map = dict()


    def __init__(self, arg):
        super(Sentiment, self).__init__()
        self.arg = arg
