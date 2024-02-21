import itertools
import pandas as pd
from pathlib import Path

# read data

def open_fn(f):
    try:
        return pd.read_csv(f,engine='python')
    except:
        return pd.DataFrame()

files1 = Path('../data/futurists_kol/data').rglob('*csv')
files2 = Path('../data/futurists_rossdawson/data').rglob('*csv')
files = itertools.chain(files1,files2)
files = list(files)

with open('account_list.txt','tr') as f:
    fpaths = f.readlines()
    fpaths = [line.strip() for line in fpaths]

files_shuffled = pd.Series(index=[f.name for f in files],data=files)
files = files_shuffled.loc[fpaths].to_list()

tweets2 = pd.concat(map(open_fn, files))
tweets2.columns = ['index','user','timestamp','url','txt']
tweets2 = tweets2.drop_duplicates(subset=['txt','timestamp'])
tweets2.reset_index(inplace=True,drop=True)

# cleaning

import html
import re
from tqdm import tqdm

regexes = [
    re.compile(
        r"(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,"
        r"}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|("
        r"?!www))[a-zA-Z0-9]+\.[^\s]{2,}|www\.[a-zA-Z0-9]+\.[^\s]{2,})"
    ), # URLS
    re.compile(r"\S*@\S*\..\S*"), # EMAILS
    re.compile(r"(?<=\s)(@[\w\-\.]+)(?=[\:\,\.\!\?\s]?)|^(@[\w\-\.]+)(?=[\:\,\.\!\?\s]?)"), # HANDLES
]

docs = tweets2['txt'].tolist()

print('Cleaning tweets... html unescape')
docs = [html.unescape(t) if t is not None else '' for t in tqdm(docs)]

for regex in regexes:
    print('Cleaning tweets... removing regex #', regexes.index(regex))
    docs = [regex.sub('', t) for t in tqdm(docs)]

print('Cleaning tweets... removing RTs')
docs = [t[4:] if t.startswith('RT :') else t for t in tqdm(docs)]

tweets2['cleaned_txt'] = docs

# test if precomputed emotions match - at random positions

import numpy as np
from transformers import pipeline

pipe = pipeline("text-classification", model="cardiffnlp/twitter-roberta-base-emotion-multilabel-latest", top_k=25)
doc2emotion = pd.read_pickle("../data/emotions_compressed.pkl.gz")

assert len(doc2emotion) == len(docs)

msg_idxs = np.random.randint(0,len(tweets2),1000)
# msg_idxs = [3] # NOTE: tweet 3 is alligned

for msg_idx in msg_idxs:

    msg = tweets2.loc[msg_idx,'cleaned_txt']
    r1 = {out['label']:out['score'] for out in pipe(msg)[0] }
    r1 = pd.DataFrame(r1.items())
    r1 = r1.set_index(0)[1].sort_index()
    
    r2 = doc2emotion.loc[msg_idx]
    r2.sort_index(inplace=True)
    assert (r2-r1).abs().mean() < 1e-2


