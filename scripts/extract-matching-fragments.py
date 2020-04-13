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
    p.add_argument('gather_matches_sig')
    p.add_argument('assembly_fasta')
    p.add_argument('--output-fragments', help='output fragments go here')
    p.add_argument('--matching-contigs', help='output contigs with ANY matches')
    p.add_argument('--nomatch-contigs', help='output contigs with NO matches')
    p.add_argument('-F', '--fragment-size', type=int, default=10000)
    args = p.parse_args()

    assert args.output_fragments

    siglist = list(sourmash.load_signatures(args.gather_matches_sig))
    print(f'loaded {len(siglist)} signatures total from {args.gather_matches_sig}')
    if not len(siglist):
        print('ERROR: need at least one matching sig; exiting')
        sys.exit(-1)

    mh_factory = siglist[0].minhash.copy_and_clear()

    print('aggregating matches...')
    combined_matches_mh = mh_factory.copy_and_clear()
    for ss in siglist:
        combined_matches_mh.merge(ss.minhash)
    print(f'...total hashes (incl not matching): {len(combined_matches_mh)}')

    print(f'outputting to: {args.output_fragments}')
    outfp = open(args.output_fragments, 'wt')

    matching_contigs = set()
    print(f'loading {args.assembly_fasta}...')
    m = 0
    for n, x in enumerate(GenomeShredder(args.assembly_fasta, args.fragment_size)):
        name, seq, start, end = x
        print(f'...on fragment {n} {name.split()[0]} start {start} - found {m} so far')

        mh = mh_factory.copy_and_clear()
        mh.add_sequence(seq, True)
        if mh.count_common(combined_matches_mh):
            m += 1
            matching_contigs.add(name)
            outfp.write(f'>frag{n}.match{m} {name} {start} {end}\n{seq}\n')

    n += 1

    outfp.close()

    print(f'found matches in {m} of {n} fragments')
    print(f'output fragments in {args.output_fragments}')
    print(f'{len(matching_contigs)} assembly contigs have matches.')

    if args.matching_contigs:
        found = 0
        print(f'outputting matching contigs to {args.matching_contigs}')
        with open(args.matching_contigs, 'wt') as fp:
            for record in screed.open(args.assembly_fasta):
                if record.name in matching_contigs:
                    found += 1
                    fp.write(f'>{record.name}\n{record.sequence}\n')

        print(f'found and output {found} matching contigs, expected {len(matching_contigs)}')
        assert found == len(matching_contigs)
    
    if args.nomatch_contigs:
        found = 0
        print(f'outputting non-matching contigs to {args.nomatch_contigs}')
        with open(args.nomatch_contigs, 'wt') as fp:
            for record in screed.open(args.assembly_fasta):
                if record.name not in matching_contigs:
                    found += 1
                    fp.write(f'>{record.name}\n{record.sequence}\n')

        print(f'found and output {found} non-matching contigs')
        #assert found == len(matching_contigs)

    return 0


if __name__ == '__main__':
    sys.exit(main())
