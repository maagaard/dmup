import sys
sys.path.insert(0, '../')
from application_only_auth import ClientException
from collections import namedtuple
from flask import Flask, render_template, request
from charting import create_date_chart
from database import database
from tsa import TSA

app = Flask(__name__)
tsa = TSA()

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

    if not hashtag:
        return render_template('mainpage.html')

    try:
        tsa.analyze_hashtag(hashtag)
        tweets = tsa.analyzed_tweets
        db_con = database.connect()
        database.create_tweets(db_con, tweets)
        chart = create_date_chart(hashtag, tsa.output_tweets()).render(is_unicode=True)
        return render_template('mainpage.html',
                               # tweets=tweets,
                               navigationitems=navigation_items,
                               chart=chart)
    except ClientException:
        # Too many request,  show something...
        return render_template('mainpage.html')


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
