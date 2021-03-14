# めんたいこTraning API設計
※現状の機能に対して、新たなサービスごとの機能切り分けが必要
## メソッド一覧

## 必要機能

### 既存機能一覧
|#|機能|既存コード|入力|出力|
|-|---|---------|---|---|
|1|BigQueryから必要なデータを取得してくる（SQL）|src/load.py|BigQuery project id|BigQuery QueryJob|
|2|Slack talkデータの整形|src/preprocess.py|整形前文字列|整形後文字列|
|3|学習用データの作成|make_dateset.py|引数なし|学習用データ (json)|
|4|Doc2Vecモデル学習|train_doc2vec.ipynb|学習用データ (json)|学習済みモデル (pkl)|
|5|各ユーザのベクタライズ|vectorize_user.py|学習済みモデル|ベクタライズ結果 (json)|
|6|学習済みモデル・ユーザデータ・ユーザベクトルのアップロード|upload_model.py|各データファイル|GCSへのアップロード|

