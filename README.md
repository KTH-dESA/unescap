# UNESCAP

## Installation

Install miniconda or conda package manager.

Create a new environment for snakemake `conda create -n snakemake -c bioconda -c conda-forge python=3.6 snakemake-minimal`

Activate the environment `conda activate snakemake`

## Running snakemake workflow

Run a dry run to see the jobs: `snakemake --dryrun`

Run the workflow in parallel: `snakemake --use-conda --cores 3`

Plot the graph of the workflow: `snakemake --use-conda --cores 3 plot_dag`
