import sys
from application_only_auth import ClientException
sys.path.insert(0, '../')

from flask import Flask, render_template, request
from collections import namedtuple
# from model import Tweet
from twitter import get_timeline

app = Flask(__name__)

NavigationItem = namedtuple('NavigationItem', ['href', 'caption'])
navigation_items = [
    NavigationItem('#', 'Home'),
    NavigationItem('top', 'Top Tweets'),
    NavigationItem('about', 'About'),
    ]


@app.route('/', methods=['GET', 'POST'])
def main_page():
    hashtag = request.form['hashtag'] if request.method == 'POST' else request.args.get('hashtag', '')

    print "Querying hashtag: " + hashtag

    try:
        tweets = get_timeline(hashtag, 10) if hashtag else []
        return render_template('mainpage.html',
                               tweets=tweets,
                               navigationitems=navigation_items)
    except ClientException:
        # Too many request, show something...
        return render_template('mainpage.html')


if __name__ == '__main__':
    # app.debug = True
    app.run(host='0.0.0.0', debug=True)
