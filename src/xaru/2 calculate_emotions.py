import pandas as pd
from transformers import pipeline
from pathlib import Path
import asyncio

repo_path = Path("/home/krajda/anticipatio/")

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

pipe = pipeline(
    "text-classification",
    model="cardiffnlp/twitter-roberta-base-emotion-multilabel-latest",
    top_k=25,
)


async def calculate(txt):
    try:
        print()
        print(txt)
        x = pipe(txt)[0]
        print(x)
        return x
    except BaseException:
        return empty


async def get_emotions():

    tweets = pd.read_pickle(repo_path / "data/final.pkl")

    docs = tweets["txt"].tolist()

    tasks = [calculate(doc) for doc in docs[3:4]]
    results = await asyncio.gather(*tasks)

    print(results)

    df = pd.DataFrame([{d["label"]: d["score"] for d in r} for r in results])
    print(df)

    df.to_pickle(repo_path / "data/emotions.pkl")


if __name__ == "__main__":
    asyncio.run(get_emotions())
