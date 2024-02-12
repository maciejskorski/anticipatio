import itertools
import pandas as pd
from pathlib import Path

from tqdm import tqdm
import json

repo_path = Path("/home/krajda/anticipatio/")


def open_fn(f):
    try:
        return pd.read_csv(f, engine="python")
    except:
        return pd.DataFrame()


files1 = Path(repo_path / "data/futurists_kol/data").rglob("*csv")
files2 = Path(repo_path / "data/futurists_rossdawson/data").rglob("*csv")
files = itertools.chain(files1, files2)
tweets = map(open_fn, files)
tweets = pd.concat(tweets)
tweets.columns = ["index", "user", "timestamp", "url", "txt"]
tweets.reset_index(drop=True, inplace=True)
tweets["txt"] = tweets["txt"].astype(str)
tweets["user"] = tweets["user"].str.replace("@", "").str.strip().str.lower()
tweets["timestamp"] = pd.to_datetime(tweets["timestamp"])
tweets.drop(columns="index", inplace=True)
tweets.drop_duplicates(inplace=True, subset=["timestamp", "txt"])
tweets.reset_index(inplace=True, drop=True)
maciek_docs = tweets["txt"]


maciek_labels = pd.read_csv(repo_path / "data/topic_labels.csv", header=None)
maciek_labels = maciek_labels[1][1:].tolist()

maciek_docs = maciek_docs.tolist()

utweets = tweets.drop_duplicates(subset=["txt"])
udocs = utweets["txt"].tolist()

mapping = []
cache = set()

for i, d in tqdm(enumerate(maciek_docs)):

    if d not in cache:
        cache.add(d)
        mapping.append([i])
    else:
        mapping[udocs.index(d)].append(i)

with open(repo_path / "data/labels_mapping.json", "w") as f:
    json.dump(mapping, f)
