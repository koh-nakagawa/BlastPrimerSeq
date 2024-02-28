
# BLAST Primer Sequence Script

## Overview

This script is designed to perform BLASTN queries for primer sequences specified in a CSV file against a designated BLAST database, compile the BLAST results into two files: `blast_primers_seq_merge.csv` and `blast_primers_seq_hit_count.csv`. This allows for a rapid assessment of primer homology against a specific BLAST database.

## Usage

### Prerequisites

- Python packages: pandas, os, subprocess, re, collections.defaultdict must be installed.
- A local BLAST database is configured.
- The input CSV file must be formatted with columns for 'primer_num', 'primer_id', and 'sequence'.

### Database Preparation

A BLAST database can be created using the `makeblastdb` command as follows:

```bash
makeblastdb -in your_sequence_data.fasta -dbtype nucl -out my_blast_db
```

### Preparing the Input CSV File

The input CSV should be formatted as follows:

```
primer_num,primer_id,sequence
1,primer1,ATCG...
2,primer2,CGTA...
```

### Running the Script

Before running the script, update the `input_csv_path`, `blast_db_path`, and `output_dir` variables to match your environment.

Executing the script will perform BLASTN queries for each primer sequence against the specified BLAST database and save the results in the output directory.

## Example Use Cases

- Checking and optimizing primer design for research purposes.
- Genomic sequence homology testing for research purposes.

## License

This script is freely available for research and commercial purposes.

## Contact

If you have any questions or need support, feel free to contact koh-nakagawa@studiokohn.com.
