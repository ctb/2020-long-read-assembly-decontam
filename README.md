# 2020-long-read-assembly-decontam

Find and extract components of long-read assemblies that match to a
database, for the purposes of decontamination.

**Still early in development.** Buyer beware! Here be dragons!!

## Installing!

You'll need snakemake and conda installed.

Then, clone this repository and change into the top-level repo directory.

### Quickstart:

Clone the repository, change into it, create the environment, and activate it:

```
git clone https://github.com/ctb/2020-long-read-assembly-decontam
cd ./2020-long-read-assembly-decontam/
conda env create -f environment.yml -n lra-decontam
conda activate lra-decontam
```

## Running!

To run, execute (in the top-level directory):

```
snakemake --use-conda -p -j 1
```

This should succeed :).

The main output files are 

Once that works, you can configure it yourself by copying
`test-data/conf-test.yml` to a new file and editing it. See
`conf/conf-necator.yml` for a real example.

## Explanation of output files.

In the output directory, there will be a few important files -- the main
ones are,

* `gather.csv` - the list of contaminants
* `matching-contigs.fa` - all contigs with any matches to the database
* `matching-fragments.fa` - all fragments with any matches to the database

## Resources

On a ~300 MB assembly, this took about 2 hours and required about 2
GB of RAM, using the
[RefSeq microbial genomes SBT](https://sourmash.readthedocs.io/en/latest/databases.html#refseq-microbial-genomes-sbt). The disk space requirement is more
significant, mainly because the SBTs are in the ~10-30 GB range when unpacked.
   
## Need help?

Please ask questions and file issues on [the sourmash GitHub issue tracker](https://github.com/dib-lab/sourmash/issues).

## Credits

Thanks to Erich Schwarz (for stubborn pursuit of contamination in
long-read assemblies) and Taylor Reiter (for stubborn pursuit of
contamination, period) for their inspiration!

A first try at this approach is detailed
[here](http://ivory.idyll.org/blog/2018-detecting-contamination-in-long-read-assemblies.html), and the discussion that led to this particular repo is in
[sourmash issue #940](https://github.com/dib-lab/sourmash/issues/940).

----

[@ctb](https://github.com/ctb/)
April 2020
