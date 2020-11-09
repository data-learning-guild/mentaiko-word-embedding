"""Make NEologd for Janome
    See:
        - https://github.com/neologd/mecab-ipadic-neologd
        - https://qiita.com/_likr/items/0fc845f59b4ad685cc06
    Prepare:
        $ git clone https://github.com/neologd/mecab-ipadic-neologd.git
        $ xz -dkv mecab-ipadic-neologd/seed/*.csv.xz
        $ cat mecab-ipadic-neologd/seed/*.csv > neologd.csv
"""

from janome.dic import UserDictionary
from janome import sysdic

print('start')
user_dict = UserDictionary('neologd.csv', 'utf8', 'ipadic', sysdic.connections)
print('made user dict object')
user_dict.save('neologd')
print('saved')
