# Summary

Contains tweets of [the futurists ranked by Ross Dawson](https://rossdawson.com/futurist/futurist-rankings/)
from January 2021 to January 2023.

Tweets are stored in the `data` subdirectory, in individual `.csv` files.

Generated with `generate.py` script.

To work with data, do:
```python
import pandas as pd
from pathlib import Path

files = Path('./data').rglob('*csv')
outs = map(pd.read_csv, files)
outs = pd.concat(outs)
outs.columns = ['index','user','timestamp','url','txt']
outs.reset_index(drop=True,inplace=True)
outs.shape # (290226, 5)
outs.head()
```