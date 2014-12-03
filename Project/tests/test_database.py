import sys
sys.path.insert(0, '../database/')
from database import database
import psycopg2

test_db = 'dmup_test'

con = None


def setup_module():
    try:
        create_db()
    except Exception as e:
        print "Could not create DB" + repr(e)


def teardown_module():
    delete_db()


def setup_func():
    con = database.connect(dbname=test_db)


def teardown_func():
    con.close()


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


def test_create_tweet():
    tweet = None
    assert(database.create_tweet(con, tweet))

def test_dummy():
    assert(True)
