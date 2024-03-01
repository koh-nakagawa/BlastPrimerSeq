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
            results = result_file.read()
            # Format results for CSV output
            formatted_results = [','.join(line.split()) for line in results.strip().split('\n')]
            blast_results[f'{primer_num}_{primer_id}'] = formatted_results

            # Count hits
            for line in formatted_results:
                evalue = float(line.split(',')[0].split('e')[1]) if 'e' in line.split(',')[0] else 0
                hit_counts[f'{primer_num}_{primer_id}']['blast_hit'] += 1
                if evalue <= -100:
                    hit_counts[f'{primer_num}_{primer_id}']['evalue_lt_e-100'] += 1
    except subprocess.CalledProcessError as e:
        print(f"Error executing BLAST for primer {primer_num} {primer_id}: {e}")

    # Cleanup
    os.remove(temp_fasta_path)


def custom_sort_key(primer_key):
    # Extended regular expression to extract primer number and direction from the primer ID,
    # including patterns for different notations of direction such as "Fw", "Rv", "forward", "reverse".
    match = re.match(r'(\D*)(\d+)([_-])?(fw|rv|F|R|forward|reverse)', primer_key, re.IGNORECASE)
    if not match:
        # If there is no match, use a default sort order.
        return (0, primer_key)

    primer_num = int(match.group(2))  # Extract the primer number.
    direction = match.group(4).lower()  # Normalize the direction to lowercase for uniformity.

    # Map various direction notations to 'fw' or 'rv'.
    direction_map = {'f': 'fw', 'fw': 'fw', 'forward': 'fw', 'r': 'rv', 'rv': 'rv', 'reverse': 'rv'}
    direction = direction_map.get(direction, direction)

    # Sort based on primer number and normalized direction.
    return (primer_num, direction)

# Use the custom sort function to sort keys.
sorted_keys = sorted(blast_results.keys(), key=custom_sort_key)

# The rest of the code (e.g., writing to files) remains unchanged.


# Write to blast_primers_seq_merge.csv
merge_output_path = os.path.join(output_dir, 'blast_primers_seq_merge.csv')
with open(merge_output_path, 'w') as merge_file:
    for key in sorted_keys:
        merge_file.write(f'>{key}\n')
        merge_file.write('evalue,sseqid\n')
        merge_file.write('\n'.join(blast_results[key]))
        merge_file.write('\n\n')

# Write hit counts to blast_primers_seq_hit_count.csv
hit_counts_output_path = os.path.join(output_dir, 'blast_primers_seq_hit_count.csv')
with open(hit_counts_output_path, 'w') as hit_counts_file:
    for key in sorted_keys:
        evalue_lt_e_100_hit = hit_counts[key]['evalue_lt_e-100']
        blast_hit = hit_counts[key]['blast_hit']
        hit_counts_file.write(f'>{key}\n')
        hit_counts_file.write('evalue<e-100_hit,blast_hit\n')
        hit_counts_file.write(f'"{evalue_lt_e_100_hit}","{blast_hit}"\n\n')
