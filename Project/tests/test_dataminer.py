"""
Only contains the structure, no tests implemented yet!
"""

import sys
sys.path.insert(0, '../')
import dataminer
from nose.tools import with_setup


def setup_module():
    pass


def teardown_module():
    pass


def setup_func():
    pass


def teardown_func():
    pass


@with_setup(setup_func, teardown_func)
def test_fetch_data():
    pass


@with_setup(setup_func, teardown_func)
def test_analyze_tweets_from_file():
    pass


@with_setup(setup_func, teardown_func)
def test_write_jsondata_to_file():
    pass


@with_setup(setup_func, teardown_func)
def test_json_from_file():
    pass


@with_setup(setup_func, teardown_func)
def test_tweets_from_json():
    pass


@with_setup(setup_func, teardown_func)
def test_write_tweets_to_file():
    pass


