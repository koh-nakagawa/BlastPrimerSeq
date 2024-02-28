
# BLAST Primer Sequence Script

## 概要

このスクリプトは、CSVファイルで指定されたプライマー配列に対してBLASTNクエリを実行し、その結果を整理して`blast_primers_seq_merge.csv`と`blast_primers_seq_hit_count.csv`という2つのファイルに出力します。これにより、特定のBLASTデータベースに対するプライマーの相同性を迅速に評価することができます。

## 使い方

### 前提条件

- Pythonパッケージ（pandas, os, subprocess, re, collections.defaultdict）がインストールされていること。
- BLASTデータベースがローカルに構成されていること。
- 入力となるCSVファイルが、`primer_num`, `primer_id`, `sequence`の列を含む形式で用意されていること。

### データベースの準備

BLASTデータベースは`makeblastdb`コマンドを使用して作成します。コマンド例は以下の通りです：

```bash
makeblastdb -in your_sequence_data.fasta -dbtype nucl -out my_blast_db
```

### 入力CSVファイルの準備

入力CSVは以下の形式である必要があります：

```
primer_num,primer_id,sequence
1,primer1,ATCG...
2,primer2,CGTA...
```

### スクリプトの実行

スクリプトを実行する前に、`input_csv_path`, `blast_db_path`, `output_dir`変数をあなたの環境に合わせて更新してください。

スクリプトを実行すると、指定したBLASTデータベースに対して各プライマー配列のBLASTNクエリが実行され、結果が出力ディレクトリに保存されます。

## 使用場面の例

- 研究目的でのゲノム配列との相同性検査
- プライマーデザインの確認と最適化

## ライセンス

このスクリプトは研究および事業目的で自由に使用していただけます。

## 連絡先

何かご不明な点やサポートが必要な場合は、koh-nakagawa@studiokohn.comまでお気軽にお問い合わせください。
