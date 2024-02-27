"""
Usage:

This script is designed to perform BLASTN queries for primer sequences contained in a specified CSV file against 
a given BLAST database, and to compile the results into a single output file named 'blast_primers_seq_merge.csv'. 
The output file includes the BLAST results for each primer, formatted and sorted according to specific criteria
(primer type and number, followed by direction).
Before running the script, ensure the input CSV file is formatted with columns for 'primer_num', 'primer_id', and
'sequence'. Update the 'input_csv_path', 'blast_db_path', and 'output_dir' variables with the paths to your input file, 
BLAST database, and desired output directory, respectively.
The script sorts the output based on primer types ('sex' or 'auto'), primer numbers, and direction ('_fw' or '_rv'), 
with a priority given to the type and number sorting over the direction.
"""

import pandas as pd
import os
import subprocess
import re
from collections import defaultdict

# Define paths for input CSV, BLAST database, and output directory
input_csv_path = '/path/to/input.csv'
blast_db_path = '/path/to/blast_db'
output_dir = '/path/to/output/dir'

# Ensure output directory exists
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Load input CSV
df = pd.read_csv(input_csv_path)

# Initialize dictionary for BLAST results
blast_results = defaultdict(list)

# Perform BLASTN for each sequence in the CSV
for index, row in df.iterrows():
    primer_num = row['primer_num']
    primer_id = row['primer_id']
    sequence = row['sequence']

    # Create temporary FASTA file for the sequence
    temp_fasta_path = os.path.join(output_dir, f'temp_{primer_num}_{primer_id}.fasta')
    with open(temp_fasta_path, 'w') as fasta_file:
        fasta_file.write(f'>{primer_id}\n{sequence}\n')

    # Set up BLASTN command
    output_path = os.path.join(output_dir, f'{primer_num}_{primer_id}.txt')
    blast_command = [
        'blastn',
        '-db', blast_db_path,
        '-query', temp_fasta_path,
        '-word_size', '6',
        '-outfmt', '6 evalue sseqid',
        '-out', output_path
    ]

    # Execute BLASTN and read results
    try:
        subprocess.run(blast_command, check=True)
        with open(output_path, 'r') as result_file:
            results = result_file.read()
            blast_results[f'{primer_num}_{primer_id}'] = results
    except subprocess.CalledProcessError as e:
        print(f"Error executing BLAST for primer {primer_num} {primer_id}: {e}")

    # Clean up temporary files
    os.remove(temp_fasta_path)
    os.remove(output_path)

# Function to sort primer results
def sort_key(filename):
    # Extract primer type, number, and direction from filename
    match = re.match(r'(sex|auto)(\d+).*(_fw|_rv)\.csv', filename)
    if match:
        prefix = match.group(1)
        number = int(match.group(2))
        direction = match.group(3)
        prefix_order = 0 if prefix == 'sex' else 1
        direction_order = 0 if direction == '_fw' else 1
        return (prefix_order, number, direction_order)
    else:
        return (2, 0, 2)

# Sort keys for output
sorted_keys = sorted(blast_results.keys(), key=sort_key)

# Write sorted results to a single output file
merged_output_path = os.path.join(output_dir, 'blast_primers_seq_merge.csv')
with open(merged_output_path, 'w') as merged_file:
    for key in sorted_keys:
        if key.endswith('.csv'):  # Include only keys ending with '.csv'
            merged_file.write(f'>{key}\n')
            merged_file.write('evalue,sseqid\n')
            merged_file.write(blast_results[key])
            merged_file.write('\n')
