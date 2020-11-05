"""This is batch script for embedding User's slack messages.
    - easiest: using spaCy trained model
    - harder but better: train custom model with spaCy or gensim
"""

import os
from pathlib import Path
from tqdm import tqdm

import pandas as pd
import spacy

from src.load import DlgDwhLoader
from src.preprocess import clean_msg


HERE = str(Path(__file__).resolve().parent)

def main():
    """word embedding for slack messages.
    """
    # load trained model
    nlp = spacy.load('ja_core_news_lg')

    # get users id list
    loader = DlgDwhLoader(os.environ['BQ_PROJECT_ID'])
    users_mart = loader.users_mart().to_dataframe()
    users = users_mart[['user_id', 'name']]

    # vectorizing messages per user
    for (i, row) in tqdm(users.iterrows()):
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
        doc = nlp(u_msgs_str)
        doc.to_disk(HERE + '/data/' + uuid + '.spdoc')


if __name__ == "__main__":
    main()

