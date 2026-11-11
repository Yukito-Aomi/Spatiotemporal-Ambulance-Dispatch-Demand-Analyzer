# -*- coding: UTF-8 -*-


import argparse
import re
from datetime import date, datetime
from pathlib import Path

import pandas as pd

from src.constants import (
    AVM_DATA_COLUMNS,
    OUTPUT_DIRECTORY_PATH,
    RAW_AVM_DATA_FILE_NAME_FORMAT,
    RAW_AVM_DATA_PATH,
    WEEKDAYS,
)


ENCODINGS = ['utf-8-sig', 'cp932']


def extract_date_from_file(input_file_path: Path) -> date | None:
    """
    ファイル名から日付を取得する関数．

    :param input_file_name:
        入力先となるファイルのパス．

    :return:
        datetime.date型で表された日付．
    """

    for file_name_format in RAW_AVM_DATA_FILE_NAME_FORMAT:
        pattern = re.escape(file_name_format)
        pattern = pattern.replace('YYYYmmdd', r'(\d{8})')

        match = re.fullmatch(pattern, input_file_path.name)

        if match:
            date_str = match.group(1)

            try:
                return datetime.strptime(date_str, '%Y%m%d').date()
            except ValueError:
                return None

    return None


def read_avm_data(input_file_path: Path) -> pd.DataFrame:
    """
    文字符号化方式を考慮してAVMデータを読み込む関数．
    
    :param input_file_path:
        入力先となるファイルのパス．
    
    :raises UnicodeError:
        規定の文字符号化方式で読み込めなかった場合
    """

    for encoding in ENCODINGS:
        try:
            return pd.read_csv(input_file_path, header=None, skiprows=1, encoding=encoding)
        except UnicodeDecodeError:
            continue

    raise UnicodeError(f'⚠️ ファイル（{input_file_path}）の文字符号化方式が規定の方式と異なります．')


def normalize_raw_data_file(
    input_file_path: Path,
    output_directory_path: Path = OUTPUT_DIRECTORY_PATH,
) -> None:
    """
    生のAVMシステムデータを正規化する関数．
    以下の処理を施す．

    - 文字符号化方式の統一
    - カラムの統一
    - 受信時刻のフォーマットの変更
    - 緯度経度のフォーマットの変更
    - ファイル名の変更

    :param input_file:
        入力先となるファイルのパス．

    :param output_directory:
        出力先となるディレクトリのパス．
    """

    # ファイル名から日付を取得する
    date_datum = extract_date_from_file(input_file_path)
    # ファイル名が規定のフォーマットと合致するかを判定する
    if date_datum is None:
        print(f'⚠️ ファイル名（{str(input_file_path)}）が規定のフォーマットと異なります．')
        return

    # 生のAVMシステムデータを読み込む
    df = read_avm_data(input_file_path)

    # カラム名を統一する
    df.columns = AVM_DATA_COLUMNS[:len(df.columns)]
    df = df.reindex(columns=AVM_DATA_COLUMNS)

    # 受信時刻のフォーマットを変換する
    df[AVM_DATA_COLUMNS[3]] = pd.to_datetime(df[AVM_DATA_COLUMNS[3]].astype('string'), format='%Y%m%d%H%M%S', errors='coerce').dt.strftime('%Y-%m-%d %H:%M:%S')

    # 緯度経度のフォーマットを変換する
    for column in [AVM_DATA_COLUMNS[4], AVM_DATA_COLUMNS[5]]:
        df[column] = pd.to_numeric(df[column], errors='coerce').div(1_000_000)
        df[column] = df[column].map(lambda value: f'{value:.6f}' if pd.notna(value) else '')

    # 出力先となるファイルのパスを設定する
    output_file_path = output_directory_path / date_datum.strftime('%Y') / date_datum.strftime('%m') / f'{date_datum.strftime("%Y%m%d")}{WEEKDAYS[date_datum.weekday()]}.csv'
    output_file_path.parent.mkdir(parents=True, exist_ok=True)

    # 正規化されたAVMシステムデータを保存する
    df.to_csv(output_file_path, index=False, encoding='utf-8-sig')

    print(f'✅ 正規化されたAVMシステムデータ（{str(output_file_path)}）を保存しました．')


def main() -> None:

    # コマンドライン引数を設定する
    parser = argparse.ArgumentParser(
        description='生のAVMシステムデータを正規化します．'
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

    args = parser.parse_args()

    # 入出力先のパスを設定する
    input_directory_path = Path(args.input_directory_path)
    output_directory_path = OUTPUT_DIRECTORY_PATH / Path(args.output_directory_path)

    # 入力先となるディレクトリの存在を確認する
    if not input_directory_path.is_dir():
        print(f'⚠️ 入力先となるディレクトリ（{str(input_directory_path)}）が存在しません．')
        return

    # 入力先となるディレクトリ内から全CSVファイルを取得する
    raw_data_files = [
        file for file in input_directory_path.rglob('*')
        if file.is_file() and file.suffix.lower() == '.csv'
    ]

    # CSVファイルの存在を確認する
    if not raw_data_files:
        print(f'⚠️ 入力先となるディレクトリ（{str(input_directory_path)}）内にCSVファイルが存在しません．')
        return

    total = len(raw_data_files)
    digit = len(str(total))

    print('> 生のAVMシステムデータを正規化します．')

    # 全AVMシステムデータを処理する
    for current, raw_data_file in enumerate(raw_data_files, start=1):
        print(f'\t> [{current:0{digit}d}/{total}] ', end='')
        normalize_raw_data_file(raw_data_file, output_directory_path)


if __name__ == '__main__':
    # `python -m src.preprocessing.normalize --output-directory-path data/avm/normalized`
    main()
