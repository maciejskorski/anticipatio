import pandas as pd
from transformers import pipeline
from pathlib import Path

repo_path = Path('/home/krajda/anticipatio/')

tweets = pd.read_pickle(repo_path / 'data/final.pkl')

docs = tweets["txt"].tolist()

pipe = pipeline(
    "text-classification",
    model="cardiffnlp/twitter-roberta-base-emotion-multilabel-latest",
    top_k=25,
)

results = []

empty = [
    {"label": "sadness", "score": 0},
    {"label": "disgust", "score": 0},
    {"label": "anger", "score": 0},
    {"label": "pessimism", "score": 0},
    {"label": "fear", "score": 0},
    {"label": "anticipation", "score": 0},
    {"label": "surprise", "score": 0},
    {"label": "joy", "score": 0},
    {"label": "optimism", "score": 0},
    {"label": "love", "score": 0},
    {"label": "trust", "score": 0},
]

for doc in docs:
    try:
        r = pipe(doc)[0]
        results.append(r)
    except BaseException:
        results.append(empty)

df = pd.DataFrame([{d["label"]: d["score"] for d in r} for r in results])
df.to_pickle(repo_path / "data/emotions.pkl")
