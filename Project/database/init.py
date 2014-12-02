"""

"""
import psycopg2


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


def create_tweet(connection, tweet):
    for hashtag in tweet['entities']['hashtags']:
        text = hashtag['text']
        print text
    raise NotImplementedError


def read_tweets_hashtag(connection, hashtag):
    raise NotImplementedError


def read_tweets_date(connection, from_date, to_date):
    raise NotImplementedError
