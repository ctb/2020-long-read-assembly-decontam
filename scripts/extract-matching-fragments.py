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
    p.add_argument('assembly')
    p.add_argument('output')
    p.add_argument('-F', '--fragment-size', type=int, default=10000)
    args = p.parse_args()

    siglist = list(sourmash.load_signatures(args.gather_matches))
    print(f'loaded {len(siglist)} signatures total from {args.gather_matches}')
    if not len(siglist):
        print('ERROR: need at least one matching sig; exiting')
        sys.exit(-1)

    mh_factory = siglist[0].minhash.copy_and_clear()

    print('aggregating matches...')
    combined_matches_mh = mh_factory.copy_and_clear()
    for ss in siglist:
        combined_matches_mh.merge(ss.minhash)
    print(f'...total hashes (incl not matching): {len(combined_matches_mh)}')

    print(f'outputting to: {args.output}')
    outfp = open(args.output, 'wt')

    print(f'loading {args.assembly}...')
    m = 0
    for n, x in enumerate(GenomeShredder(args.assembly, args.fragment_size)):
        name, seq, start, end = x
        print(f'...{n} {name.split()[0]} {start} - found {m} so far')

        mh = mh_factory.copy_and_clear()
        mh.add_sequence(seq)
        if mh.count_common(combined_matches_mh):
            m += 1
            outfp.write(f'>frag{n}.match{m} {name} {start} {end}\n{seq}\n')

    n += 1

    outfp.close()

    print(f'found matches in {m} of {n} fragments')
    print(f'output in {args.output}')
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
