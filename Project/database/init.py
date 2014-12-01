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

    # should switch from datatype 'json' to 'jsonb' when using Postgres >9.4
    # and apply GIN for better query performance
    execute_sql(connection,
                "CREATE TABLE tweets (id serial, polarity double precision, tweetdata json)")
