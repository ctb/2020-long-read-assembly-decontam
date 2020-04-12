#
# use with --use-conda for maximal froodiness.
#

# override this with --configfile on command line
configfile: 'test-data/conf.yml'

outputdir = config['outputdir'].rstrip('/') + '/'
scaled = config['scaled']
ksize = config['ksize']

genomes_location = config['database_matching_genomes']

all_matching_files = []
for root, dirs, files in os.walk(genomes_location, topdown=False):
    for name in files:
        filename = os.path.join(root, name)
        if filename.startswith('./'): filename = filename[2:]
        all_matching_files.append(filename)


rule gather_all:
    input:
        query = outputdir + 'contigs.sig',
        database = config['database']
    output:
        csv = outputdir + 'gather.csv',
        matches = outputdir + 'matches.sig'
    conda: 'conf/env-sourmash.yml'
    params:
        scaled = scaled
    shell: """
        sourmash gather {input.query} {input.database} -o {output.csv} \
            --save-matches {output.matches} --scaled={params.scaled}
    """

rule extract_fragments:
    input:
        matches = outputdir + 'matches.sig',
        genomes = all_matching_files
    shell: """
        ./scripts/extract-matching-fragments.py {input.matches} {input.genomes}
    """

rule contigs_sig:
    input:
        config['assembly']
    output:
        outputdir + 'contigs.sig'
    conda: 'conf/env-sourmash.yml'
    params:
        scaled = scaled,
        ksize = ksize
    shell: """
        sourmash compute -k {params.ksize} --scaled {params.scaled} \
            {input} -o {output}
    """