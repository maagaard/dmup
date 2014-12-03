"""

"""
import sys
sys.path.insert(0, '../')
import psycopg2
import model
import json
# from debug import DLOG
from dateutil.parser import *


def DLOG(msg):
    print msg


def connect(dbname="dmup", user="dmup", password="dmup123"):
    """Connects to a PostgreSQL database and returns the connection"""
    return psycopg2.connect(database=dbname, user=user, password=password)


def execute_sql(connection, sql):
    """Executes an SQL query, sql, on connection"""
    cur = connection.cursor()
    cur.execute(sql)
    connection.commit()
    cur.close()


def create_database(connection):
    """Creates the database used in the DMUP project"""
    execute_sql(connection,
                "CREATE DATABASE dmup WITH OWNER 'dmup'")


def create_user(connection):
    """Creates the user used in the DMUP project"""
    execute_sql(connection,
                "CREATE ROLE dmup WITH LOGIN CREATEDB PASSWORD 'dmup123'")


def create_tables(connection):
    """Creates the tables used in the DMUP project

    Tables are created on the database in connection"""

    cur = connection.cursor()
    # should switch from datatype 'json' to 'jsonb' when using Postgres >9.4
    # and apply GIN for better query performance
    cur.execute("""
    CREATE TABLE tweets
    (
      id serial NOT NULL,
      created timestamp with time zone,
      polarity double precision,
      data json,
      CONSTRAINT tweets_pkey PRIMARY KEY (id)
    )
    WITH (
      OIDS=FALSE
    );
    """)

    cur.execute("""
    CREATE TABLE hashtags
    (
      id serial NOT NULL,
      hashtag character varying(139),
      polarity double precision,
      CONSTRAINT hashtags_pkey PRIMARY KEY (id),
      CONSTRAINT hashtags_hashtag_key UNIQUE (hashtag)
    )
    WITH (
      OIDS=FALSE
    );
    """)

    cur.execute("CREATE INDEX hashtag_idx ON hashtags(hashtag)")

    cur.execute("""
    CREATE TABLE tweet_hashtag
    (
      tweet_id integer NOT NULL,
      hashtag_id integer NOT NULL,
      CONSTRAINT tweet_hashtag_pkey PRIMARY KEY (tweet_id, hashtag_id),
      CONSTRAINT tweet_hashtag_hashtag_id_fkey FOREIGN KEY (hashtag_id)
          REFERENCES hashtags (id) MATCH SIMPLE
          ON UPDATE NO ACTION ON DELETE NO ACTION,
      CONSTRAINT tweet_hashtag_tweet_id_fkey FOREIGN KEY (tweet_id)
          REFERENCES tweets (id) MATCH SIMPLE
          ON UPDATE NO ACTION ON DELETE NO ACTION
    )
    WITH (
      OIDS=FALSE
    );
    """)

    connection.commit()
    cur.close()


"""
Insert a tweet into the database in connection

TODO: Do not insert tweets already in the database
TODO: Exception handling on cur.execute()
"""


def create_tweet(connection, tweet, polarity=0):
    cur = connection.cursor()
    hashtag_ids = []
    # Insert hashtags if they do not already exist, and get the IDs of all hashtags for tweet
    for hashtag in tweet.entities['hashtags']:
        hashtag_text = hashtag['text']
        cur.execute('SELECT COUNT(*) FROM hashtags WHERE hashtag = \'%s\'' % hashtag_text)
        count = cur.fetchone()[0]
        try:
            if count == 0:  # Insert and get IDs
                cur.execute('INSERT INTO hashtags (polarity, hashtag) VALUES (%s, %s) RETURNING id',
                            (0, hashtag_text))
                hashtag_ids.append(cur.fetchone()[0])
            else:  # Get IDs only
                cur.execute('SELECT id FROM hashtags WHERE hashtag = \'%s\'' % hashtag_text)
                hashtag_ids.append(cur.fetchone()[0])

            DLOG("Inserted hashtag: " + hashtag_text)

        except Exception as e:
            DLOG("Could not add hashtag to database: " + repr(e))
            return

    # Insert the tweet into the database
    tweet.user = None
    try:
        cur.execute('INSERT INTO tweets (created, polarity, data) VALUES (\'%s\', %s, \'%s\') RETURNING id'
                    % (parse(tweet.created_at), polarity, json.dumps(tweet.__dict__)))
        tweet_id = cur.fetchone()[0]

        DLOG("Inserted tweet with id: " + str(tweet_id))

    except Exception as e:
        DLOG("Could not add tweet to database: " + repr(e))
        return

    # Insert relations between tweet and hashtags
    try:
        for hashtag_id in hashtag_ids:
            cur.execute('INSERT INTO tweet_hashtag (tweet_id, hashtag_id) VALUES (%s, %s)'
                        % (tweet_id, hashtag_id))
            DLOG("Inserted tweet/hashtag relation with id: " + tweet_id + "-" + hashtag_id)

    except Exception as e:
        DLOG("Could not add tweet/hashtag relation to database: " + repr(e))
        return

    connection.commit()
    cur.close()


def read_tweets_hashtag(connection, hashtag):
    cur = connection.cursor()
    sql = """
        SELECT tweets.id, tweets.created, tweets.data
        FROM hashtags
        INNER JOIN tweet_hashtag
            ON tweet_hashtag.hashtag_id = hashtags.id
        INNER JOIN tweets
            ON tweets.id = tweet_hashtag.tweet_id
        WHERE hashtag = \'%s\'
    """ % hashtag
    print sql
    cur.execute(sql)
    print cur.fetchone()[0]


def read_tweets_date(connection, from_date, to_date):
    raise NotImplementedError
