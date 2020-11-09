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
- [Uploading objects with gsutil | Google Cloud Docs][gsutil_cp_to_gcs]
- [Uploading objects with python | Google Cloud Docs][upload_to_gcs_python]
- [gsutil cp | Google Cloud Reference][gsutil_cp_ref]
- [Creating buckets with gsutil | Google Cloud Docs][gsutil_mb]
- [Creating buckets with python | Google Cloud Docs][create_bucket_python]
- [GCS Storage classes | Google Cloud Docs][gcs_storage_classes]

[spacy_usage]: https://spacy.io/usage
[spacy_models]: https://spacy.io/models
[spacy_api]: https://spacy.io/api
[spacy_univ]: https://spacy.io/universe
[spacy_course]: https://course.spacy.io/ja/
[python_client_for_gbq]: https://googleapis.dev/python/bigquery/latest/index.html
[pandas_gbq_and_gbq]: https://cloud.google.com/bigquery/docs/pandas-gbq-migration?hl=ja
[gsutil_cp_to_gcs]: https://cloud.google.com/storage/docs/uploading-objects?hl=ja#gsutil
[gsutil_cp_ref]: https://cloud.google.com/storage/docs/gsutil/commands/cp
[gsutil_mb]: https://cloud.google.com/storage/docs/creating-buckets?hl=ja
[gcs_storage_classes]: https://cloud.google.com/storage/docs/storage-classes
[upload_to_gcs_python]: https://cloud.google.com/storage/docs/uploading-objects#storage-upload-object-python
[create_bucket_python]: https://cloud.google.com/storage/docs/creating-buckets#storage-create-bucket-code_samples

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
# make dataset
python make_dataset.py

# on Google Colab
# upload dataset (./data/train_dataset.json)
# exec notebooks/train_doc2vec.ipynb
# download model (./data/trained_doc2vec.model)

# vectorize user's posts
python vectorize_user.py

# matching simulation - with cmd args
python matching_simulator.py --cmd Pythonに詳しいのは誰？

# matching simulation - with a file
# $ cat question.txt
# Pythonに詳しいのは誰？
python matching_simulator.py --file question.txt

# matching simulation - with user id
python matching_simulator.py --user U01N5N64NNN
```

---

## Deployment

- Create a bucket
- Upload objects to the bucket

```bash
python upload_model.py
```
