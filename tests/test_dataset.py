import pandas as pd
from pathlib import Path


def test_all_scraped():
    """Test if all futurists data are present """

    # accounts to scrape
    user_names = pd.read_csv('data/futurists_koe/2023_03_09_The Key Opinion Leaders anticipating the future.txt', sep=r'\s(?=@)')
    user_names.reset_index(inplace=True)
    user_names.columns = ['name','account']

    # accounts already scraped
    scrapped_accounts = Path('data/futurists_koe/data').glob('*csv')
    scrapped_accounts = set(t.stem for t in scrapped_accounts)
    
    # compare
    requested_accounts = set(user_names['account'])
    user_names = requested_accounts.difference(scrapped_accounts)
    user_names.remove(None)
    assert user_names == set()

def test_scraped_nonempty():
    """Check if downloaded data are nonempty"""
    
    # accounts already scraped
    scrapped_accounts = Path('data/futurists_koe/data').glob('*csv')
    for t in scrapped_accounts:
        df = pd.read_csv('data/futurists_koe/data/@OttLegalRebels.csv',engine='python')
        assert len(df) > 1
    
    