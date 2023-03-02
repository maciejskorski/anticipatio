# Datasets

* [Futurists from Ross Dawson's Influence Rankings](./futurists_rossdawson/)
* [Key Opinion Leader list](./futurists_koe/)

To work with data:
```python
import pandas as pd
from pathlib import Path

files = Path('./futurists_koe/data').rglob('*csv')
outs = map(pd.read_csv, files)
outs = pd.concat(outs)
outs.columns = ['index','user','timestamp','url','txt']
outs.reset_index(drop=True,inplace=True)
outs.shape # (290226, 5)
outs.head()
```