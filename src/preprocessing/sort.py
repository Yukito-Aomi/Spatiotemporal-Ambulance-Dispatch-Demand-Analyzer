# -*- coding: UTF-8 -*-


import argparse
from datetime import datetime
from pathlib import Path

import pandas as pd

from src.constants import (
    OUTPUT_DIRECTORY_PATH,
    RAW_AVM_DATA_PATH,
    WEEKDAYS,
)


ENCODING = 'utf-8-sig'


def sort_asc(input_file_path: Path, columns: list[str], output_directory_path: Path = OUTPUT_DIRECTORY_PATH) -> None:
    """
    正規化されたAVMシステムデータを指定された列ごとに昇順で並び替える関数．

    :param input_file:
        入力先となるファイルのパス．

    :param columns:
        カラム名．

    :param output_directory:
        出力先となるディレクトリのパス．
    """

    # 正規化されたAVMシステムデータを読み込む
    df = pd.read_csv(input_file_path, encoding=ENCODING)

    # 列の存在を確認する
    if [col for col in columns if col not in df.columns]:
        raise ValueError(f'⚠️ 指定されたカラムが存在しません．')
    # 指定された列ごとに昇順で並び替える
    df = df.sort_values(by=columns, ascending=True)

    # ファイル名から日付を取得する
    date_datum = datetime.strptime(input_file_path.stem[:8], '%Y%m%d').date()
    # 出力先となるファイルのパスを設定する
    output_file_path = output_directory_path / date_datum.strftime('%Y') / date_datum.strftime('%m') / f'{date_datum.strftime("%Y%m%d")}{WEEKDAYS[date_datum.weekday()]}.csv'
    output_file_path.parent.mkdir(parents=True, exist_ok=True)

    # AVMシステムデータを保存する
    df.to_csv(output_file_path, index=False, encoding=ENCODING)

    print(f'✅ AVMシステムデータ（{str(output_file_path)}）を保存しました．')


def main() -> None:

    # コマンドライン引数を設定する
    parser = argparse.ArgumentParser(
        description='正規化されたAVMシステムデータを任意の列ごとに昇順で並び替えます．'
    )
    parser.add_argument(
        '--input-directory-path',
        type=str,
        default=RAW_AVM_DATA_PATH,
        help='入力先となるディレクトリのパス',
    )
    parser.add_argument(
        '--output-directory-path',
        type=str,
        default='',
        help='出力先となるディレクトリのパス',
    )
    parser.add_argument(
        '--columns',
        type=str,
        nargs='+',
        required=True,
        help='カラム名（複数指定可能）',
    )

    args = parser.parse_args()

    # 入出力先のパスを設定する
    input_directory_path = Path(args.input_directory_path)
    output_directory_path = OUTPUT_DIRECTORY_PATH / Path(args.output_directory_path)

    # 入力先となるディレクトリの存在を確認する
    if not input_directory_path.is_dir():
        print(f'⚠️ 入力先となるディレクトリ（{str(input_directory_path)}）が存在しません．')
        return

    # 入力先となるディレクトリ内から全CSVファイルを取得する
    data_files = [
        file for file in input_directory_path.rglob('*')
        if file.is_file() and file.suffix.lower() == '.csv'
    ]

    # CSVファイルの存在を確認する
    if not data_files:
        print(f'⚠️ 入力先となるディレクトリ（{str(input_directory_path)}）内にCSVファイルが存在しません．')
        return

    total = len(data_files)
    digit = len(str(total))

    print(f'> 正規化されたAVMシステムデータを列（{'・'.join(args.columns)}）ごとに昇順で並び替えます．')

    # 全AVMシステムデータを処理する
    for current, file in enumerate(data_files, start=1):
        print(f'\t> [{current:0{digit}d}/{total}] ', end='')
        sort_asc(input_file_path=file, columns=args.columns, output_directory_path=output_directory_path)


if __name__ == '__main__':
    # `python -m src.preprocessing.sort --input-directory-path output/data/avm/normalized --output-directory-path data/avm/sorted --columns 車両コード 受信時刻`
    main()
