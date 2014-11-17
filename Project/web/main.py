import sys
sys.path.insert(0, '../')

from flask import Flask, render_template, request
from collections import namedtuple
# from model import Tweet
from twitter import get_timeline

app = Flask(__name__)


# class NavigationItem:
#     def __init__(self, href, caption):
#         self.href = href
#         self.caption = caption

NavigationItem = namedtuple("NavigationItem", ['href', 'caption'])


@app.route('/')
def main_page():
    hashtag = request.args.get('hashtag', '')
    return render_template('mainpage.html',
                           tweets=get_timeline(hashtag, 10)
                           if hashtag else [])

if __name__ == '__main__':
    # app.debug = True
    app.run(host='0.0.0.0', debug=True)
