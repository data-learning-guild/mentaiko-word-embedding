"""word embedding core
    - easiest: using spaCy trained model
    - harder but better: train custom model with spaCy or gensim
"""

import os

import spacy
from src.load import DlgDwhLoader


def main():
    nlp = spacy.load('ja_core_news_lg')
    doc = nlp('わたしは山田太郎ですよ。')
    for token in doc:
        print(token.i, ', ', token.text, ', ', token.pos_)
    
    loader = DlgDwhLoader(os.environ['BQ_PROJECT_ID'])
    msgs = loader.msgs_by_user(user_id='UJKFAPBCJ', ch_join_msg=False)
    print(msgs.to_dataframe())


if __name__ == "__main__":
    main()

