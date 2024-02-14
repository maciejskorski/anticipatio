import pandas as pd
from pathlib import Path


def test_all_scraped():
    """Test if all futurists data are present """

    # accounts to scrape
    user_names = pd.read_csv('data/futurists_kol/2023_03_09_The Key Opinion Leaders anticipating the future.txt', sep=r'\s(?=@)')
    user_names.reset_index(inplace=True)
    user_names.columns = ['name','account']

    # accounts already scraped
    scrapped_accounts = Path('data/futurists_kol/data').glob('*csv')
    scrapped_accounts = set(t.stem for t in scrapped_accounts)
    
    # compare
    requested_accounts = set(user_names['account'])
    user_names = requested_accounts.difference(scrapped_accounts)
    user_names.remove(None)
    assert user_names == set()

def test_scraped_nonempty():
    """Check if downloaded data are nonempty"""
    
    # accounts to scrape
    scrapped_accounts = pd.read_csv('data/futurists_kol/2023_03_09_The Key Opinion Leaders anticipating the future.txt', sep=r'\s(?=@)')
    scrapped_accounts = set(scrapped_accounts['List of Key Opinion Leaders anticipating the future'])
    scrapped_accounts.remove(None)
    
    data_dir = Path('data/futurists_kol/data')
    for account in scrapped_accounts:
        try:
            df = pd.read_csv(data_dir/(account+'.csv'),engine='python')
            assert len(df) > 1
        except:
            print(account)

def test_dataset_order():
    """Check dataset indexing """

    def open_fn(f):
        try:
            return pd.read_csv(f,engine='python')
        except:
            return pd.DataFrame()

    tweets = pd.concat([
        pd.concat(map(open_fn, Path('../data/futurists_kol/data').rglob('*csv'))),
        pd.concat(map(open_fn, Path('../data/futurists_rossdawson/data').rglob('*csv')))
    ])

    tweets.columns = ['index','user','timestamp','url','txt']
    tweets = tweets.drop_duplicates(subset=['txt'])
    tweets.reset_index(inplace=True,drop=True)

    print(tweets.loc[3,'txt'])
    