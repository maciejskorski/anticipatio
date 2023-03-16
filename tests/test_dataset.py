import pandas as pd
import os


def test_all_scrapped():
    """Test if all futurists data are present """

    # accounts to scrape
    user_names = pd.read_csv('data/futurists_koe/2023_03_09_The Key Opinion Leaders anticipating the future.txt', sep=r'\s(?=@)')
    user_names.reset_index(inplace=True)
    user_names.columns = ['name','account']

    # accounts already scraped

    scrapped_accounts = os.listdir('data/futurists_koe/data')
    scrapped_accounts = set(t.split('.csv')[0] for t in scrapped_accounts)
    requested_accounts = set(user_names['account'])

    user_names = requested_accounts.difference(scrapped_accounts)
    user_names.remove(None)

    assert user_names == set()
