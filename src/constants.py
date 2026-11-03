# -*- coding: UTF-8 -*-


from pathlib import Path


# 生のAVMシステムデータのパス
RAW_AVM_DATA = Path('resources/data/avm/raw')
# 前処理されたのAVMシステムデータのパス
PREPROCESSED_AVM_DATA = Path('resources/data/avm/preprocessed')

# 出力先となるディレクトリのパス
OUTPUT_DIRECTORY = Path('output')

# 名古屋市の中心座標
CENTER_POINT_NAGOYA = [35.181441,136.907173]

# 初期ズームレベル
ZOOM_START = 13
