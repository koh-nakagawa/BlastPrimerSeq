# PrimerSeqBlast

BLAST Primer Sequences Script README
English
Overview
This script performs BLASTN queries for primer sequences listed in a specified CSV file against a designated BLAST database. The results are compiled into a single output file named 'blast_primers_seq_merge.csv', which includes the BLAST results for each primer, formatted and sorted according to specific criteria (primer type and number, followed by direction).

Prerequisites
Python 3
Pandas library
BLAST+ command line tools installed and accessible in your environment
Input File Format
Ensure the input CSV file is formatted with columns for 'primer_num', 'primer_id', and 'sequence'.

Configuration
Update the input_csv_path, blast_db_path, and output_dir variables within the script with the paths to your input file, BLAST database, and desired output directory, respectively.

Running the Script
Execute the script using Python from the terminal:

bash
Copy code
python /path/to/blast_primer_seq_merge.py
Output
The script will generate a file named 'blast_primers_seq_merge.csv' in the specified output directory. This file contains the sorted BLAST results for each primer.


日本語
概要
このスクリプトは、指定されたCSVファイルにリストされたプライマー配列に対して指定されたBLASTデータベースに対するBLASTNクエリを実行し、'blast_primers_seq_merge.csv'という単一の出力ファイルに結果をまとめます。このファイルには、特定の基準（プライマータイプと番号、方向に続く）に従ってフォーマットされ並べ替えられた各プライマーのBLAST結果が含まれます。

前提条件
Python 3
Pandas ライブラリ
BLAST+ コマンドラインツールがインストールされ、環境内でアクセス可能であること
入力ファイルの形式
入力CSVファイルが 'primer_num'、'primer_id'、および 'sequence' の列でフォーマットされていることを確認してください。

設定
スクリプト内の input_csv_path、blast_db_path、および output_dir 変数を、それぞれ入力ファイル、BLASTデータベース、および希望の出力ディレクトリへのパスに更新してください。

スクリプトの実行
ターミナルからPythonを使用してスクリプトを実行します：

bash
Copy code
python /path/to/blast_primer_seq_merge.py
出力
スクリプトは指定された出力ディレクトリに 'blast_primers_seq_merge.csv' というファイルを生成します。このファイルには、各プライマーのソートされたBLAST結果が含まれます。

