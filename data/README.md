# Datasets

* [Futurists from Ross Dawson's Influence Rankings](./futurists_rossdawson/), from January 2021 to January 2023.
* [Key Opinion Leader list](./futurists_koe/), from January 2021 to January 2023.

To work with datasets:
```python
import pandas as pd
from pathlib import Path

def open_fn(f):
    try:
        return pd.read_csv(f,engine='python')
    except:
        return pd.DataFrame()

files = Path('../futurists_rossdawson/data').rglob('*csv')
outs = map(open_fn, files)
outs = pd.concat(outs)
outs.columns = ['index','user','timestamp','url','txt']
outs.reset_index(drop=True,inplace=True)
print(outs['user'].nunique(),len(outs)) # 184 users, 290226 tweets
outs.head()

files = Path('../futurists_koe/data').rglob('*csv')
outs = map(open_fn, files)
outs = pd.concat(outs)
outs.columns = ['index','user','timestamp','url','txt']
outs.reset_index(drop=True,inplace=True)
print(outs['user'].nunique(),len(outs)) # 233 users, 1203189 tweets
outs.head()
```