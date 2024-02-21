import json as json
import pandas as pd
from pathlib import Path
import en_core_web_sm
from tqdm import tqdm 

repo_path = Path('/home/krajda/anticipatio/')
tweets = pd.read_pickle(repo_path / 'data/final.pkl')
docs = tweets["txt"].tolist()

nlp = en_core_web_sm.load()

lemmas = []
lemmas_pos = []
ents = []
ent_types = []

for doc in tqdm(nlp.pipe(docs, n_process=-1)):
    lemmas.append([token.lemma_ for token in doc if not any([token.is_stop, token.is_punct, token.is_space, token.is_digit, token.is_currency, token.like_num, token.like_email, token.like_url])])
    lemmas_pos.append([token.pos_ for token in doc if not any([token.is_stop, token.is_punct, token.is_space, token.is_digit, token.is_currency, token.like_num, token.like_email, token.like_url])])
    ents.append([str(doc[ent.start:ent.end]) for ent in doc.ents if ent.label_ not in ["CARDINAL", "DATE", "QUANTITY", "TIME", "PERCENT", "ORDINAL"]])
    ent_types.append([ent.label_ for ent in doc.ents if ent.label_ not in ["CARDINAL", "DATE", "QUANTITY", "TIME", "PERCENT", "ORDINAL"]])

with open(repo_path / 'data/lemmas.json', 'w') as f:
    json.dump(lemmas, f)
with open(repo_path / 'data/ents.json', 'w') as f:
    json.dump(ents, f)
with open(repo_path / 'data/ent_types.json', 'w') as f:
    json.dump(ent_types, f)
with open(repo_path / 'data/lemmas_pos.json', 'w') as f:
    json.dump(lemmas_pos, f)