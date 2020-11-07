"""vector matching simulator
    - 各ユーザーの発言と質問文の類以度を計算し、類以度の高い順にレコメンドするシミュレーターCLI
    - 本スクリプトをベースに本番システムのソースコードを記述する
"""

import argparse
import json
import os
import sys
from pathlib import Path

import pandas as pd
import spacy

from src.load import DlgDwhLoader


HERE = str(Path(__file__).resolve().parent)

def overlap(_x: list, _y: list) -> float:
    """overlap coefficient
        Szymkiewicz-Simpson coefficient)
        https://en.wikipedia.org/wiki/Overlap_coefficient
    """
    set_x = frozenset(_x)
    set_y = frozenset(_y)
    return len(set_x & set_y) / float(min(map(len, (set_x, set_y))))

def main(input_text: str):
    # vectorize input_text with trained model
    nlp = spacy.load('ja_core_news_lg')
    doc_key = nlp(input_text)
    vec_key = doc_key.vector.tolist()

    # search the most similar doc (Top 5)
    p = Path(HERE)
    vec_file_list = list(p.glob('./data/*.json'))
    uuid_l = []
    similarity_l = []
    for vec_file_path in vec_file_list:
        uuid = vec_file_path.stem
        uuid_l.append(uuid)

        with open(str(vec_file_path), 'r', encoding='utf-8') as f:
            cur_vec = json.load(f)

        similarity = overlap(vec_key, cur_vec)
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

    args = parser.parse_args()
    if (args.cmd is None) and (args.file is None):
        print('at least one of the two args. --cmd or --file.')
        sys.exit(1)

    # set input text
    input_text = ''
    if args.cmd is not None:
        input_text = args.cmd
        if args.file is not None:
            print('set one of the two. --cmd or --file')
            sys.exit(1)
    elif args.file is not None:
        with open(args.file, 'r', encoding='utf-8') as f:
            input_text = f.read()
        if args.cmd is not None:
            print('set one of the two. --cmd or --file')
            sys.exit(1)

    # main proc
    main(input_text)
