# portfolio-word-embedding
文章の分散表現モデル

See:

- [spaCy Usage][spacy_usage]
- [spaCy Models][spacy_models]
- [spaCy API][spacy_api]
- [spaCy Universe][spacy_univ]
- [spaCy Course][spacy_course]
- [BQ Python client org][python_client_for_gbq]
- [pandas-gbq からの移行 | Google Cloud Docs][pandas_gbq_and_gbq]

[spacy_usage]: https://spacy.io/usage
[spacy_models]: https://spacy.io/models
[spacy_api]: https://spacy.io/api
[spacy_univ]: https://spacy.io/universe
[spacy_course]: https://course.spacy.io/ja/
[python_client_for_gbq]: https://googleapis.dev/python/bigquery/latest/index.html
[pandas_gbq_and_gbq]: https://cloud.google.com/bigquery/docs/pandas-gbq-migration?hl=ja

---

## Features

- Download slack messages from slack DWH on BigQuery
- NLP preparation: Remove Noses, Morphological Analysis ... and so on.
- Build word embedding model with doc2vec.

---

## Build Environment

install spaCy

```bash
pip install -U spacy
# japanese core news model (large size)
python -m spacy download ja_core_news_lg
```

---

## Learning

---

## Usage

```bash
# activate virtual env
source env/bin/activate
# set environ values
source ./set-envval.sh
# vectorize user's posts
python vectorize_user.py
# matching simulation
python matching_simulator.py --cmd Pythonに詳しいのは誰？
python matching_simulator.py --file question.txt
python matching_simulator.py --user U01N5N64NNN
```
