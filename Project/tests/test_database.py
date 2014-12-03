import sys
sys.path.insert(0, '../database/')
from database import database
import psycopg2
from offlinedata import read_json_from_file, tweets_from_json
from nose.tools import with_setup

test_db = 'dmup_test'

tweets = tweets_from_json(read_json_from_file('Project/testdata/starwars_pos.json'))

def setup_module():
    try:
        create_db()
    except Exception as e:
        print "Could not create DB: " + repr(e)


def teardown_module():
    try:
        delete_db()
    except Exception as e:
        print "Could not delete DB: "  + repr(e)


def create_db():
    con = psycopg2.connect(database='postgres', user='dmup', password='dmup123')
    con.set_isolation_level(0)
    database.create_database(con, test_db)
    con.close()
    con = database.connect(dbname=test_db)
    database.create_tables(con)


def delete_db():
    con = psycopg2.connect(database='postgres', user='dmup', password='dmup123')
    con.set_isolation_level(0)
    database.execute_sql(con, 'DROP DATABASE %s' % test_db)

def delete_db_data():
    con = database.connect(dbname=test_db)
    database.execute_sql(con, 'DELETE FROM tweet_hashtag')
    database.execute_sql(con, 'DELETE FROM tweets')
    database.execute_sql(con, 'DELETE FROM hashtags')


def test_create_tweet():
    con = database.connect(dbname=test_db)
    t = tweets[6]
    assert(database.create_tweet(con, t))
    cur = con.cursor()
    cur.execute('SELECT id FROM tweets WHERE created = \'%s\'' % t.created_at)
    id = cur.fetchone()[0]
    assert(id > 0)
    delete_db_data()


def test_create_tweets():
    con = database.connect(dbname=test_db)
    ts = tweets
    inserted = database.create_tweets(con, ts)
    #assert(inserted = len(tweets))
    print "Inserted count: " + str(inserted)
    cur = con.cursor()
    cur.execute('SELECT COUNT(*) FROM tweets')
    count = cur.fetchone()[0]
    assert(count == 10)
    delete_db_data()


def test_read_tweets_hashtag():
    assert(False)


def test_read_tweets_date():
    assert(False)
