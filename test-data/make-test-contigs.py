#! /usr/bin/env python
import screed, sys

fp = open('test-contigs.fa', 'wt')

for n, record in enumerate(screed.open('63.fa')):
    for i in range(0, len(record.sequence), 100000):
        fragment = record.sequence[i:i+100000]
        fp.write(f'>seq{n}.{i}\n{fragment}\n')

fp.close()
