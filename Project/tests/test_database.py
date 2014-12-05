"""
Tests in this module requires a PostgreSQL database >=9.3 running on port 5432,
as well as a ROLE with name 'dmup', password 'dmup123' with permissions LOGIN and CREATEDB.
Databases and tables will be created and deleted automatically.
"""
import sys
sys.path.insert(0, '../database/')
from database import database
from offlinedata import read_json_from_file, tweets_from_json
from datetime import datetime
import psycopg2
from nose.tools import with_setup

test_db = 'dmup_test'
tweets = tweets_from_json(read_json_from_file('Project/testdata/starwars_pos.json')) + tweets_from_json(read_json_from_file('Project/testdata/starwars_neg.json'))


con = None


def setup_module():
    try:
        create_db()
    except Exception as e:
        print "Could not create DB: " + repr(e)


def teardown_module():
    try:
        delete_db()
    except Exception as e:
        print "Could not delete DB: " + repr(e)


def create_db():
    global con
    con = psycopg2.connect(database='postgres', user='dmup', password='dmup123')
    con.set_isolation_level(0)
    database.create_database(con, test_db)
    con.close()
    con = database.connect(dbname=test_db)
    database.create_tables(con)


def delete_db():
    global con
    con = psycopg2.connect(database='postgres', user='dmup', password='dmup123')
    con.set_isolation_level(0)
    database.execute_sql(con, 'DROP DATABASE %s' % test_db)


def connect_db():
    global con
    con = database .connect(dbname=test_db)

    
def delete_db_data():
    global con
    database.execute_sql(con, 'DELETE FROM tweet_hashtag')
    database.execute_sql(con, 'DELETE FROM tweets')
    database.execute_sql(con, 'DELETE FROM hashtags')
    con.close()


@with_setup(connect_db, delete_db_data)
def test_create_tweet():
    global con
    t = tweets[6]
    assert(database.create_tweet(con, t))
    cur = con.cursor()
    cur.execute('SELECT id FROM tweets WHERE created = \'%s\'' % t.created_at)
    id = cur.fetchone()[0]
    assert(id > 0)


@with_setup(connect_db, delete_db_data)
def test_create_tweets():
    global con
    ts = tweets
    inserted = database.create_tweets(con, ts)
    assert(inserted == len(ts))
    cur = con.cursor()
    cur.execute('SELECT COUNT(*) FROM tweets')
    count = cur.fetchone()[0]
    assert(count == len(ts))


@with_setup(connect_db, delete_db_data)
def test_update_hashtag_polarity():
    global con
    t = tweets[8]
    database.create_tweet(con, t)
    database.update_hashtag_polarity(con, t.hashtags[0], 0.1337)
    cur = con.cursor()
    cur.execute('SELECT polarity FROM hashtags WHERE hashtag = \'%s\'' % t.hashtags[0])
    assert(cur.fetchone()[0] == 0.1337)


@with_setup(connect_db, delete_db_data)
def test_read_tweets_hashtag():
    global con
    inserted = database.create_tweets(con, tweets[10:20])
    assert(inserted == 10)
    res = database.read_tweets_hashtag(con, 'starwars')
    assert(len(res) == 10)


@with_setup(connect_db, delete_db_data)
def test_read_tweets_date():
    global con
    database.create_tweets(con, tweets)
    res = database.read_tweets_date(con, datetime(2014, 12, 1, 12, 19, 0), datetime.now())
    assert(len(res) == 13)
