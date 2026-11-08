# -*- coding: UTF-8 -*-


import argparse
from pathlib import Path

import folium
from dotenv import load_dotenv

from src.constants import (
    CENTER_POINT_NAGOYA,
    OUTPUT_DIRECTORY,
    ZOOM_START
)


OUTPUT_FILE_NAME = 'maps/default_map.html'


def generate_default_map(
    output_path: str = str(OUTPUT_DIRECTORY / Path(OUTPUT_FILE_NAME)),
    zoom_start: int = ZOOM_START
) -> None:    
    """
    名古屋市の地図を生成する関数．

    :param output_path:
        出力先のパス．

    :zoom_start:
        地図の初期ズームレベル．
    """

    # 地図オブジェクトを生成する
    map = folium.Map(
        location=CENTER_POINT_NAGOYA,
        zoom_start=zoom_start,
    )

    # 地図オブジェクトを書き出す 
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    map.save(output_path)

    print(f'✅ 名古屋市の地図（{output_path}）を保存しました．')


def main() -> None:

    # コマンドライン引数を設定する
    parser = argparse.ArgumentParser(
        description='名古屋市の地図を生成します．'
    )
    parser.add_argument(
        '--output-file-name',
        type=str,
        default=OUTPUT_FILE_NAME,
        help='出力される地図のファイル名',
    )
    parser.add_argument(
        '--zoom-start',
        type=int,
        default=int(ZOOM_START),
        help='地図の初期ズームレベル',
    )
    args = parser.parse_args()

    # 出力先のパスを設定する
    output_path = OUTPUT_DIRECTORY / Path(args.output_file_name)

    # 地図を生成する
    generate_default_map(str(output_path), int(args.zoom_start))


if __name__ == '__main__':
    # `python -m src.visualization.create_base_map`
    main()
