#
# use with --use-conda for maximal froodiness.
#

# override this with --configfile on command line
configfile: 'test-data/conf.yml'

outputdir = config['outputdir'].rstrip('/') + '/'
scaled = config['scaled']
ksize = config['ksize']

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
