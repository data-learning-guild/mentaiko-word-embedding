# portfolio-word-embedding
文章の分散表現モデル

See:

- [spaCy Usage][spacy_usage]
- [spaCy Models][spacy_models]
- [spaCy API][spacy_api]
- [spaCy Universe][spacy_univ]
- [spaCy Course][spacy_course]

[spacy_usage]: https://spacy.io/usage
[spacy_models]: https://spacy.io/models
[spacy_api]: https://spacy.io/api
[spacy_univ]: https://spacy.io/universe
[spacy_course]: https://course.spacy.io/ja/

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


