import pygal
from pygal.style import DarkGreenBlueStyle


def create_bar_chart(hashtag, tweets):
    bar_chart = pygal.Bar(style=DarkGreenBlueStyle)
    bar_chart.title = "Sentiment for #%s over time" % hashtag
    bar_chart.x_labels = map(str, range(11))
    bar_chart.add('TEST', [{'value': 30, 'label': 'sup'}, 2])
    bar_chart.add('Fibonacci', [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55])
    bar_chart.add('Padovan', [1, 1, 1, 2, 2, 3, 4, 5, 7, 9, 12])
    return bar_chart


def create_date_chart(hashtag, tweet_bins):
    date_chart = pygal.DateY(x_label_rotation=45)
    date_chart.title = "Sentiment for #%s over time" % hashtag
    res = []
    for bin in tweet_bins:
        if(len(bin) > 0):
            avg = sum(map(lambda x: x.polarity, bin)) / len(bin)
            res.append((bin[0].get_date(), avg))

    date_chart.add('sentiment', res)
    date_chart.x_labels_format = "%Y-%m-%d"

    return date_chart
