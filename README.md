
# BLAST Primer Sequence Analysis Tool

## Overview
This tool performs BLASTN queries for primer sequences specified in a CSV file against a designated BLAST database. It compiles the results into two output files:
- `blast_primers_seq_merge.csv`: Contains the BLAST results for each primer, formatted and sorted. This includes making evalue and sseqid values comma-separated for easy CSV handling.
- `blast_primers_seq_hit_count.csv`: Lists counts of BLAST hits with evalues less than e-100 and total BLAST hits for each primer.

## Usage
1. Ensure your input CSV file is formatted with columns for 'primer_num', 'primer_id', and 'sequence'.
2. Update the `input_csv_path`, `blast_db_path`, and `output_dir` variables in the script with the paths to your input file, BLAST database, and desired output directory, respectively.
3. Run the script to perform the BLAST queries and generate the output files.

## Requirements
- Python 3.x
- Pandas library
- Local BLAST+ command line tool installed and configured

## Configuration
- `input_csv_path`: Path to the input CSV file containing primer sequences.
- `blast_db_path`: Path to the BLAST database against which the queries will be run.
- `output_dir`: Directory where the output files will be saved.

## Output Files
- `blast_primers_seq_merge.csv`: Sorted BLAST results for each primer, with evalue and sseqid values separated by commas for easy handling.
- `blast_primers_seq_hit_count.csv`: Counts of hits with evalues < e-100 and total hits, providing a quick overview of significant matches.

## License
This tool is released under the MIT License.
