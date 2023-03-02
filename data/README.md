# Datasets

* [Futurists from Ross Dawson's Influence Rankings](./futurists_rossdawson/)
* [Key Opinion Leader list](./futurists_koe/)

To work with datasets:
```python
import pandas as pd
from pathlib import Path

import pandas as pd
from pathlib import Path

files = Path('futurists_rossdawson/data').rglob('*csv')
outs = map(pd.read_csv, files)
outs = pd.concat(outs)
outs.columns = ['index','user','timestamp','url','txt']
outs.reset_index(drop=True,inplace=True)
print(outs['user'].nunique(),len(outs)) # 184 users, 290226 tweets
outs.head()

files = Path('futurists_koe/data').rglob('*csv')
for f in files:
    try:
        _ = pd.read_csv(f)
    except:
        print(f)

outs = map(pd.read_csv, files)
outs = pd.concat(outs)
outs.columns = ['index','user','timestamp','url','txt']
outs.reset_index(drop=True,inplace=True)
print(outs['user'].nunique(),len(outs)) # ?
outs.head()
```