#! /usr/bin/env python
import screed, sys

fp = open('test-contigs.fa', 'wt')

for record in screed.open('63.fa'):
    for i in range(0, len(record.sequence), 100000):
        fragment = record.sequence[i:i+100000]
        fp.write(f'>seq{i}\n{fragment}\n')

fp.close()
