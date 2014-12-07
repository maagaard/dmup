__author__ = "Emil Maagaard & Bjarke Vad Andersen"
__credits__ = []
__version__ = "1.0"

import sys
sys.path.insert(0, '../')
from application_only_auth import ClientException
from collections import namedtuple
from flask import Flask, render_template, request, g
from charting import create_date_chart
import database
import tsa
from tsa import sort_tweets
from debug import DLOG
import pickle

app = Flask(__name__)
tsa = tsa.TSA()

NavigationItem = namedtuple('NavigationItem', ['href', 'caption'])
navigation_items = [
    NavigationItem('#', 'Home'),
    NavigationItem('top', 'Top Tweets'),
    NavigationItem('about', 'About'),
]


def get_db():
    """
    Gets a database connection for the current request
    """
    if not hasattr(g, 'db_con'):
        g.db_con = database.connect()
        return g.db_con


@app.teardown_appcontext
def close_db(error):
    """
    Closes the database after the current request
    """
    if(error):
        DLOG("Teardown error: " + str(error))

    # tsa.set_analyzed_tweets(None)
    if hasattr(g, 'db_con'):
        g.db_con.close()


@app.route('/', methods=['GET', 'POST'])
def main_page():
    hashtag = request.form['hashtag'] if request.method == 'POST' else request.args.get('hashtag', '')

    if not hashtag:
        return render_template('mainpage.html', navigationitems=navigation_items)

    try:
        tsa.analyze_hashtag(hashtag, count=100)
        DLOG("Querying hashtag: " + hashtag)
        tweets = tsa.analyzed_tweets
        db_con = get_db()
        database.create_tweets(db_con, tweets)
        chart = create_date_chart(hashtag, tsa.output_tweets()).render(is_unicode=True)
        return render_template('mainpage.html',
                               # tweets=tweets,
                               navigationitems=navigation_items,
                               chart=chart)
    except ClientException:
        # Too many request,  show something...
        return render_template('mainpage.html', error='Twitter API exhausted, please wait (max. 15 minutes)')
    except Exception as e:
        DLOG("Something went wrong: " + repr(e))
        return render_template('mainpage.html')


@app.route('/layoutdebug')
def layoutdebug():
    chart = create_date_chart('DEBUG', []).render(is_unicode=True)
    return render_template('mainpage.html',
                           # tweets=tweets,
                           navigationitems=navigation_items,
                           chart=chart)

def filtershort(tweets):
    if(len(tweets) < 10):
        return []
    else:
        return tweets

def chart_file(filename, hashtag):
    file = open(filename)
    tweets = pickle.load(file)
    file.close()
    tsa.set_output_mode('hours')
    tsa.set_analyzed_tweets(tweets)
    atweets = map(filtershort, tsa.output_tweets())
    return create_date_chart(hashtag, atweets).render_response(is_unicode=True)

@app.route('/ferguson')
def ferguson():
    return chart_file('Ferguson-slim.pkl', 'Ferguson')

@app.route('/obama')
def obama():
    return chart_file('Obama-slim.pkl', 'Obama')

if __name__ == '__main__':
    # app.debug = True
    tmp_con = database.connect(user='postgres', password='', dbname='postgres')

    try:
        tmp_con.set_isolation_level(0)
        database.create_user(tmp_con)
    except Exception as e:
        tmp_con.close()
        tmp_con = database.connect(user='postgres', password='', dbname='postgres')
        print repr(e)

    try:
        tmp_con.set_isolation_level(0)
        database.create_database(tmp_con)
    except Exception as e:
        print repr(e)

        tmp_con.close()
        tmp_con = database.connect()

    try:
        database.create_tables(tmp_con)
    except Exception as e:
        print repr(e)

    app.run(host='0.0.0.0', debug=True)
