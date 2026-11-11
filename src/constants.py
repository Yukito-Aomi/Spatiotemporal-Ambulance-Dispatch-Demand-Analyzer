# -*- coding: UTF-8 -*-


from pathlib import Path


"""曜日"""
WEEKDAYS = [
    'mo',  # 月曜日
    'tu',  # 火曜日
    'we',  # 水曜日
    'th',  # 木曜日
    'fr',  # 金曜日
    'sa',  # 土曜日
    'su',  # 日曜日
]
"""生のAVMシステムデータのファイル名のフォーマット"""
RAW_AVM_DATA_FILE_NAME_FORMAT = (
    'AVM_Location_YYYYmmdd_無害化済.csv',
    'AVM_Location_YYYYmmdd_操作履歴記録.csv',
    'AVM_Location_YYYYmmdd.csv',
)
"""AVMシステムデータのカラム名"""
AVM_DATA_COLUMNS = [
    '署所名称',
    '車両コード',
    '車両名称',
    '受信時刻',
    '緯度',
    '経度',
    '動態',
    '車両方位',
    '走行速度',
    '事案番号',
]

"""生のAVMシステムデータのパス"""
RAW_AVM_DATA_PATH = Path('resources/data/avm/raw')
"""前処理されたのAVMシステムデータのパス"""
PREPROCESSED_AVM_DATA_PATH = Path('resources/data/avm/preprocessed')
"""出力先となるディレクトリのパス"""
OUTPUT_DIRECTORY_PATH = Path('output')

"""名古屋市の中心座標"""
CENTER_POINT_NAGOYA = [35.181441,136.907173]
"""初期ズームレベル"""
ZOOM_START = 13
