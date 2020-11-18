"""vector matching simulator
    - 各ユーザーの発言と質問文の類以度を計算し、類以度の高い順にレコメンドするシミュレーターCLI
    - 本スクリプトをベースに本番システムのソースコードを記述する
"""


import argparse
import io
import json
import os
import pickle
import sys
from pathlib import Path
from typing import List, Set, Dict, Tuple, TypeVar

import google.auth
import numpy as np
import pandas as pd
import spacy
from gensim.models.doc2vec import Doc2Vec
from google.oauth2 import service_account
from google.cloud import storage
from janome.tokenizer import Tokenizer

from src.load import DlgDwhLoader
from src.preprocess import clean_msg


class GoogleCloudStorage():
    '''
    Google Cloud Storage操作に関するクラス
    Google Cloud StorageのデータをダウンロードしてPythonのデータ型に変換する
    Pythonのデータ型をアップロードしてGoogle Cloud Storageのデータに変換する
    '''
    def __init__(self, parameter: Dict=None) -> None:
        '''
        App Engine サービスアカウントのデフォルト認証情報を使う
        '''
        if parameter is None:
            self.client = storage.Client()
            buckets = list(self.client.list_buckets())
            print(buckets)
        else:
            self.project_name = parameter['project']
            self.bucket_name = parameter['bucket']
            self.file_name = parameter['folder']
            self.mime_type = parameter['mime_type']
            self.credential_path = parameter['credential_path']


        try:
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = str((Path(Path.cwd()).parent)/parameter["credential_path"])
            self.credentials = str((Path(Path.cwd()).parent)/parameter["credential_path"])
            self.client = storage.Client(self.project_name).from_service_account_json(self.credentials)
        except Exception as e:
            print(e)

        try:
            self.credentials, _ = google.auth.default()
            self.client = storage.Client(project=self.project_name, credentials=self.credentials)
        except Exception as e:
            print(e)

        try:
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = str((Path(Path.cwd()).parent)/parameter["credential_path"])
            self.credentials, _ = google.auth.default()
            if self.credentials.requires_scopes:
                self.credentials = self.credentials.with_scopes(['https://www.googleapis.com/auth/devstorage.read_write'])
            self.client = storage.Client(credentials=self.credentials)
        except Exception as e:
            print(e)

        try:
            credentials_path = str((Path(Path.cwd()).parent)/parameter["credential_path"])
            self.credentials = service_account.Credentials.from_service_account_file(credentials_path)
            if self.credentials.requires_scopes:
                self.credentials = self.credentials.with_scopes(['https://www.googleapis.com/auth/devstorage.read_write'])
            self.client = storage.Client(credentials=self.credentials)
        except Exception as e:
            print(e)


    def download_as_string(self) -> str:
        bucket = self.client.get_bucket(self.bucket_name)
        blob = storage.Blob(self.file_name, bucket)
        return blob.download_as_string()

    def download_as_pickle(self) -> str:
        bucket = self.client.get_bucket(self.bucket_name)
        blob = storage.Blob(self.file_name, bucket)
        return pickle.loads(blob.download_as_string())

    def download_to_file(self, file_obj) -> object:
        bucket = self.client.get_bucket(self.bucket_name)
        blob = storage.Blob(self.file_name, bucket) 
        return blob.download_to_file(file_obj)

    def upload_from_string(self, context: str) -> None:
        bucket = self.client.get_bucket(self.bucket_name)
        blob = storage.Blob(self.file_name, bucket)
        blob.upload_from_string(context, content_type=self.mime_type)

    def upload_from_ndjson(self, dataframe: pd.core.frame.DataFrame) -> None:
        '''
        GCSからBigQueryにあげるときにndjson形式だとエラーが発生しにくい為、
        pandas.DataFrameをndjson形式で保存できるようにしている
        '''
        buffer = io.StringIO()
        dataframe.to_json(buffer, orient="records", lines=True, force_ascii=False)
        bucket = self.client.get_bucket(self.bucket_name)
        blob = storage.Blob(self.file_name, bucket)
        blob.upload_from_string(buffer.getvalue(), content_type=self.mime_type)

    def upload_from_file(self, file_obj) -> None:
        bucket = self.client.get_bucket(self.bucket_name)
        blob = storage.Blob(self.file_name, bucket)
        blob.upload_from_file(file_obj)


HERE = str(Path(__file__).resolve().parent)
t = Tokenizer()

def overlap(_x: list, _y: list) -> float:
    """overlap coefficient (Unuse)
        Szymkiewicz-Simpson coefficient)
        https://en.wikipedia.org/wiki/Overlap_coefficient
    """
    set_x = frozenset(_x)
    set_y = frozenset(_y)
    return len(set_x & set_y) / float(min(map(len, (set_x, set_y))))

def cos_similarity(_x: list, _y: list) -> float:
    """cos similarity for small value
    """
    vx = np.array(_x) * 10000
    vy = np.array(_y) * 10000
    return np.dot(vx, vy) / (np.linalg.norm(vx) * np.linalg.norm(vy))

def main(input_text: str, input_uid: str):
    key_vector = []
    model = Doc2Vec.load('./data/trained_doc2vec.model')
    
    # set key vector
    if input_text is not None:
        # vectorize input_text with trained model
        # spaCy version: # nlp = spacy.load('ja_core_news_lg')
        # spaCy version: # doc_key = nlp(input_text)
        # spaCy version: # key_vector = doc_key.vector.tolist()
        cleaned_text = clean_msg(input_text)
        cleaned_text_wakati = list(t.tokenize(cleaned_text, wakati=True))
        key_vector = model.infer_vector(cleaned_text_wakati).tolist()
    elif input_uid is not None:
        p = Path('./data/{}.json'.format(input_uid))
        if p.exists():
            with open('./data/{}.json'.format(input_uid), 'r') as f:
                key_vector = json.load(f)
        else:
            print('user_id is invalid.')
            return
    
    # search the most similar doc (Top 5)
    p = Path(HERE)
    vec_file_list = list(p.glob('./data/*.json'))
    uuid_l = []
    similarity_l = []
    for vec_file_path in vec_file_list:
        if input_uid is not None:
            # 同じベクトルのCOS類以度は計算しない
            if input_uid == vec_file_path.stem:
                continue
        if vec_file_path.stem in ['dataset', 'test_dataset', 'train_dataset']:
            continue
        
        uuid = vec_file_path.stem
        uuid_l.append(uuid)

        with open(str(vec_file_path), 'r', encoding='utf-8') as f:
            cur_vec = json.load(f)

        similarity = cos_similarity(key_vector, cur_vec)
        similarity_l.append(similarity)

    df_sim_tbl = pd.DataFrame({'user_id': uuid_l, 'similarity': similarity_l})
    df_sim_tbl = df_sim_tbl.sort_values('similarity', ascending=False)
    
    # DEBUG
    df_sim_tbl.to_csv('user_sim_tbl.csv', index=False)

    # output top 5 users
    df_sim_tbl_top5 = df_sim_tbl.head(5)
    loader = DlgDwhLoader(os.environ['BQ_PROJECT_ID'])
    users_mart = loader.users_mart().to_dataframe()
    users_id_mst = users_mart[['user_id', 'name']]
    
    print('============================')
    print('Top 5 users.')
    print('name\tuuid\tsimilarity')
    print('----------------------------')
    for (i, row) in df_sim_tbl_top5.iterrows():
        uuid = row['user_id']
        similarity = row['similarity']
        uname = users_id_mst[users_id_mst['user_id'] == uuid]['name'].iloc[0]
        print('{0}\t{1}\t{2}'.format(uname, uuid, similarity))


if __name__ == "__main__":
    """simulator entrypoint
        - arg0: __file__
        - arg1: input text
    """
    # parse args
    parser = argparse.ArgumentParser(description='vector matching simulator')
    parser.add_argument('--cmd', required=False, help='matching key str from cmd arg')
    parser.add_argument('--file', required=False, help='matching key str from file')
    parser.add_argument('--user', required=False, help='indicate matching key vector with user id.')

    args = parser.parse_args()
    if (args.cmd is None) and (args.file is None) and (args.user is None):
        print('at least one of the two args. --cmd or --file.')
        sys.exit(1)

    # set input text
    input_text = None
    input_uid = None
    if args.cmd is not None:
        input_text = args.cmd
        if (args.file is not None) or (args.user is not None):
            print('set one of the three. --cmd or --file or --user')
            sys.exit(1)
    elif args.file is not None:
        with open(args.file, 'r', encoding='utf-8') as f:
            input_text = f.read()
        if (args.cmd is not None) or (args.user is not None):
            print('set one of the three. --cmd or --file or --user')
            sys.exit(1)
    elif args.user is not None:
        input_uid = args.user
        if (args.cmd is not None) or (args.file is not None):
            print('set one of the three. --cmd or --file or --user')
            sys.exit(1)

    # main proc
    main(input_text, input_uid)
