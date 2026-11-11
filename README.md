# Spatiotemporal Ambulance Dispatch Demand Analyzer

救急自動車の走行履歴を活用した救急出動需要の時空間解析システム．

## 開発環境の構築

本プロジェクトは，以下の技術を使用する．

- Python 3.13.13
- HTML

### バージョン管理されていないファイルの設置

プログラムの実行にあたり，以下のファイルを設置する必要がある．

- 📁 resources/data/avm/raw/

### Pythonのインストール

Pythonをインストールする．
推奨するバージョンはPython 3.13.13である．

1. Python 3.13.13をインストールする

```
# 省略
```

2. Pythonのバージョンを確認する

```
python -V
```

### 仮想環境の作成

仮想環境を作成する．

1. 仮想環境を作成する

```
python -m venv .venv
```

2. 仮想環境を有効化する

```
source .venv/bin/activate
```

> [!NOTE]
> `which python`コマンドを実行することでPythonコマンドの実行ファイルのパスを確認できる．

> [!NOTE]
> `deactivate`コマンドを実行することで仮想環境を無効化できる．

3. パッケージをインストールする

```
pip install -r requirements.txt
```

> [!NOTE]
> `pip freeze > requirements.txt`コマンドを実行することでrequirements.txtを更新できる．

## プログラムの実行方法

### AVMシステムデータの前処理

1. 生のAVMシステムデータを正規化する

```
python -m src.preprocessing.normalize --output-directory-path data/avm/normalized
```

2. 正規化されたAVMシステムデータを車両コードごとに時系列順にソートする

```
python -m src.preprocessing.sort --input-directory-path output/data/avm/normalized --output-directory-path data/avm/sorted --columns 車両コード 受信時刻
```

### 地図の生成

未実装．

```
# 動作確認用のプログラム
python -m src.visualization.create_base_map
```

### 救急出動需要の学習および推定

未実装．

## プロジェクトの設計および仕様

### ディレクトリ構造

- 📁 Spatiotemporal-Ambulance-Dispatch-Demand-Analyzer/
  - 📁 .venv/
  - 📁 output/
  - 📁 resources/data/avm/raw/
  - 📁 src/
    - 📁 preprocessing/
      - 📄 normalize.py
      - 📄 sort.py
    - 📁 visualization/
      - 📄 create_base_map.py
    - 📄 constants.py
  - 📄 .gitignore
  - 📄 README.md
  - 📄 requirements.txt

### AVMシステムデータ

AVMシステムデータとは，車両管理システム「AVM（Automatic Vehicle Monitoring）システム」から取得されるCSV形式で表された救急自動車の走行履歴である．

> [!NOTE]
> 正規化されたAVMシステムデータのファイル名は，年月日を表す8桁の数字に曜日を表す2文字のアルファベットを加えた形式に統一される．
> また，これらのデータのカラムは以下の通りである．
>
> | 署所名称 | 車両コード | 車両名称 | 受信時刻 | 緯度 | 経度 | 動態 | 車両方位 | 走行速度 | 事案番号 |
> |---|---|---|---|---|---|---|---|---|---|
> | … | … | … | … | … | … | … | … | … | … |
