"""
blast_primer_seq_merge.py

Usage:

This script is designed to perform BLASTN queries for primer sequences contained in a specified CSV file against
a given BLAST database, compile the BLAST results into a single output file named 'blast_primers_seq_merge.csv',
and generate an additional file named 'blast_primers_seq_hit_count.csv'. The latter file includes counts of BLAST hits
with evalues less than e-100 and total BLAST hits for each primer.

Before running the script, ensure:
- The input CSV file is formatted with columns for 'primer_num', 'primer_id', and 'sequence'.
- The 'input_csv_path', 'blast_db_path', and 'output_dir' variables are updated with the paths to your input file,
  BLAST database, and desired output directory, respectively.

The script sorts the output based on primer types ('sex' or 'auto'), primer numbers, and direction ('_fw' or '_rv'),
with a priority given to the type and number sorting over the direction.

Outputs:
- 'blast_primers_seq_merge.csv': Contains the formatted BLAST results for each primer.
- 'blast_primers_seq_hit_count.csv': Contains counts of hits with evalues < e-100 and total hits for each primer.

Requirements:
- Python packages: pandas, os, subprocess, re, collections.defaultdict
- A local BLAST database configured with the specified path in 'blast_db_path'.
- Input CSV file with primer information at the specified path in 'input_csv_path'.
"""


import pandas as pd
import os
import subprocess
import re
from collections import defaultdict

# Paths
input_csv_path = '/path/to/your/input.csv'
blast_db_path = '/path/to/your/blast_db'
output_dir = '/path/to/your/output_dir'

# Create output directory if not exists
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Read the input CSV
df = pd.read_csv(input_csv_path)

# Dictionary to hold BLAST results and hit counts
blast_results = defaultdict(list)
hit_counts = defaultdict(lambda: {'evalue_lt_e-100': 0, 'blast_hit': 0})

# Execute BLASTN for each sequence
for index, row in df.iterrows():
    primer_num = row['primer_num']
    primer_id = row['primer_id']
    sequence = row['sequence']

    # Temporary FASTA file path
    temp_fasta_path = os.path.join(output_dir, f'temp_{primer_num}_{primer_id}.fasta')
    with open(temp_fasta_path, 'w') as fasta_file:
        fasta_file.write(f'>{primer_id}\n{sequence}\n')

    # BLASTN command
    output_path = os.path.join(output_dir, f'{primer_num}_{primer_id}.txt')
    blast_command = [
        'blastn',
        '-db', blast_db_path,
        '-query', temp_fasta_path,
        '-word_size', '6',
        '-outfmt', '6 evalue sseqid',
        '-out', output_path
    ]

    try:
        subprocess.run(blast_command, check=True)
        with open(output_path, 'r') as result_file:
            for line in result_file:
                evalue, sseqid = line.split()
                evalue_num = float(evalue.split('e')[1]) if 'e' in evalue else 0
                blast_results[f'{primer_num}_{primer_id}'].append(line.strip())
                hit_counts[f'{primer_num}_{primer_id}']['blast_hit'] += 1
                if evalue_num <= -100:
                    hit_counts[f'{primer_num}_{primer_id}']['evalue_lt_e-100'] += 1
    except subprocess.CalledProcessError as e:
        print(f"Error executing BLAST for primer {primer_num} {primer_id}: {e}")

    # Cleanup
    os.remove(temp_fasta_path)
    os.remove(output_path)

# Function to sort keys as before
def sort_key(filename):
    # Similar sorting function as before

# Sorted keys based on custom sort function (not shown fully for brevity)
sorted_keys = sorted(blast_results.keys(), key=sort_key)

# Write to a single file (blast_primers_seq_merge.csv)
# Similar to previous functionality, not shown for brevity

# New functionality: Write hit counts to a new file
hit_counts_output_path = os.path.join(output_dir, 'blast_primers_seq_hit_count.csv')
with open(hit_counts_output_path, 'w') as hit_counts_file:
    for key in sorted_keys:
        evalue_lt_e_100_hit = hit_counts[key]['evalue_lt_e-100']
        blast_hit = hit_counts[key]['blast_hit']
        hit_counts_file.write(f'>{key}.csv\n')
        hit_counts_file.write('evalue<e-100_hit,blast_hit\n')
        hit_counts_file.write(f'"{evalue_lt_e_100_hit}","{blast_hit}"\n\n')
