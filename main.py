"""word embedding core
    - easiest: using spaCy trained model
    - harder but better: train custom model with spaCy or gensim
"""

import spacy



def main():
    nlp = spacy.load('ja_core_news_lg')
    doc = nlp('わたしは山田太郎ですよ。')
    for token in doc:
        print(token.i, ', ', token.text, ', ', token.pos_)


if __name__ == "__main__":
    main()

