"""This is batch script for embedding User's slack messages.
    - easiest: using spaCy trained model
    - harder but better: train custom model with spaCy or gensim
"""

import json
import os
import pickle
from pathlib import Path

from gensim.models.doc2vec import Doc2Vec
from janome.tokenizer import Tokenizer
import pandas as pd
import spacy
from tqdm import tqdm

from src.load import DlgDwhLoader
from src.preprocess import clean_msg


HERE = str(Path(__file__).resolve().parent)
t = Tokenizer()

def main():
    """word embedding for slack messages.
    """
    # load trained model
    # spaCy version: # nlp = spacy.load('ja_core_news_lg')
    model = Doc2Vec.load('./data/trained_doc2vec.model')

    # get users id list
    loader = DlgDwhLoader(os.environ['BQ_PROJECT_ID'])
    users_mart = loader.users_mart().to_dataframe()
    users = users_mart[['user_id', 'name']]
    with open('./data/users.csv.pkl', 'wb') as f:
        pickle.dump(users, f)

    # vectorizing messages per user
    for (i, row) in tqdm(list(users.iterrows()), desc='[save vector]'):
        # get per user
        uuid = row['user_id']
        uname = row['name']
        u_msgs = loader.msgs_by_user(user_id=uuid, ch_join_msg=False).to_dataframe()[['user_id', 'text']]

        # concat all of posted messages
        u_msgs_str = ' '.join(u_msgs['text'].values.tolist())

        # remove noise
        u_msgs_str = clean_msg(u_msgs_str)

        # vectorize
        # > https://spacy.io/api/doc
        # > https://spacy.io/api/vectors
        # spaCy version: # doc = nlp(u_msgs_str)
        # spaCy version: # vector = doc.vector.tolist()
        u_msgs_str_wakati = list(t.tokenize(u_msgs_str, wakati=True))
        vector = model.infer_vector(u_msgs_str_wakati).tolist()
        with open(HERE + '/data/' + uuid + '.json', 'w', encoding='utf-8') as f:
            json.dump(vector, f, indent=2)
        

if __name__ == "__main__":
    main()

