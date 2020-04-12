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
        csv = outputdir + 'gather.csv'
    shell: """
        sourmash gather {input.query} {input.database} -o {output.csv}
    """

rule contigs_sig:
    input:
        config['assembly']
    output:
        outputdir + 'contigs.sig'
    shell: """
        sourmash compute -k 31 --scaled {scaled} -k {ksize} {input} -o {output}
    """
