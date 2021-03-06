#!/usr/bin/env python3

import argparse
import collections
from Bio import SeqIO
import os
import csv
cwd = os.getcwd()



def parse_args():
    parser = argparse.ArgumentParser(description='Check DB for query sequences.')

    parser.add_argument("--query", action="store", type=str, dest="query")
    parser.add_argument("--seqs", action="store", type=str, dest="seqs")
    parser.add_argument("--metadata", action="store", type=str, dest="metadata")
    parser.add_argument("--data-column", action="store", type=str, dest="data_column")
    parser.add_argument("--input-column", action="store", type=str, dest="input_column")
    parser.add_argument("--in-metadata", action="store", type=str, dest="in_metadata")
    parser.add_argument("--in-seqs", action="store", type=str, dest="in_seqs")
    parser.add_argument("--not-in-db", action="store", type=str, dest="not_in_db")
    return parser.parse_args()

def check_db():
    args = parse_args()

    found = []
    
    in_metadata = []
    in_metadata_names = []
    
    query_names = []
    with open(args.query,newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            query_names.append(row[args.input_column])

    with open(args.metadata,newline="") as f:
        reader = csv.DictReader(f)
        header_names = reader.fieldnames
        for row in reader:
            for seq in query_names:

                db_id = row[args.data_column]
                if seq == db_id:
                    
                    row["query"]=row[args.data_column]
                    row["closest"]=row[args.data_column]
                    in_metadata.append(row)
                    in_metadata_names.append(seq)

    print(f"Number of query records found in metadata: {len(in_metadata)}")
    with open(args.in_metadata, "w") as fw:
        header_names.append("query")
        header_names.append("closest")
        writer = csv.DictWriter(fw, fieldnames=header_names,lineterminator='\n')
        writer.writeheader()
        writer.writerows(in_metadata)

    with open(args.in_seqs, "w") as fw:
        for record in SeqIO.parse(args.seqs, "fasta"):
            for name in in_metadata_names:
                if name==record.id:
                    found.append(name)
                    fw.write(f">{name} status=in_db\n{record.seq}\n")
    print(f"Number of associated sequences found: {len(found)}")
    with open(args.not_in_db, "w") as fw:
        print("\nThe following sequences were not found in the database:")
        fw.write(f"{args.input_column}\n")
        for query in query_names:
            if query not in found:
                fw.write(query + '\n')
                print(f"\t-{query}")
        print("If you wish to access sequences in the database\nwith your query, ensure the sequence names match the names in the metadata format.")


if __name__ == '__main__':

    check_db()