# install social media scrapper: !pip3 install snscrape
import snscrape.modules.twitter as sntwitter
import itertools
import multiprocessing as mp
import datetime
import pandas as pd
import logging

# configure logging
logging.basicConfig()
logger = logging.getLogger('scrapping')
logger.setLevel(logging.INFO)


# twits ranges
start_date = datetime.datetime(2021,1,1,tzinfo=datetime.timezone.utc)
attributes = ('date','url','rawContent')


def get_tweets(username,n_tweets=None,attributes=attributes):
    tweets = sntwitter.TwitterSearchScraper(f'from:{username}').get_items() # invoke the scrapper
    tweets = itertools.islice(tweets,n_tweets) # stopped when the count reached
    tweets = itertools.takewhile(lambda t:t.date>=start_date, tweets) # stop when date passed
    tweets = map(lambda t: (username,)+tuple(getattr(t,a) for a in attributes),tweets) # keep only attributes needed
    pd.DataFrame(tweets).to_csv(f'./data/{username}.csv')
    logger.info(username)
    return tweets


# a list of accounts to scrape
user_names = pd.read_csv('./2023_03_09_The Key Opinion Leaders anticipating the future.txt', sep=r'\s(?=@)')
user_names.reset_index(inplace=True)
user_names.columns = ['name','account']

import os
scrapped_accounts = os.listdir('data')
scrapped_accounts = set(t.split('.csv')[0] for t in scrapped_accounts)
requested_accounts = set(user_names['account'])

user_names = requested_accounts.difference(scrapped_accounts)


# parallelise queries for speed ! 
with mp.Pool(4) as p:
    results = p.imap(get_tweets, user_names)
    p.close()
    p.join()