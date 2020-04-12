#! /usr/bin/env python
import argparse
import sys

import sourmash
import screed

class GenomeShredder(object):
    def __init__(self, genome_file, fragment_size):
        self.genome_file = genome_file
        self.fragment_size = fragment_size

    def __iter__(self):
        fragment_size = self.fragment_size

        for record in screed.open(self.genome_file):
            if not fragment_size:
                yield record.name, record.sequence, 0, len(record.sequence)
            else:
                for start in range(0, len(record.sequence), fragment_size):
                    seq = record.sequence[start:start + fragment_size]
                    yield record.name, seq, start, start + len(seq)


def main():
    p = argparse.ArgumentParser()
    p.add_argument('gather_matches')
    p.add_argument('genomes', nargs='+')
    args = p.parse_args()

    siglist = list(sourmash.load_signatures(args.gather_matches))
    print(f'loaded {len(siglist)} signatures total from {args.gather_matches}')
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
