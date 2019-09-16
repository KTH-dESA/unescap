# UNESCAP

## OSeMOSYS Workflow

### Installation

Install miniconda or conda package manager.

Create a new environment for snakemake `conda create -n snakemake -c bioconda -c conda-forge python=3.6 snakemake-minimal`

Activate the environment `conda activate snakemake`

### Running snakemake workflow

Run a dry run to see the jobs: `snakemake --dryrun`

Run the workflow in parallel: `snakemake --use-conda --cores 3`

Plot the graph of the workflow: `snakemake --use-conda --cores 3 plot_dag`

# Dashboard instructions
A companion dashboard to visualize the results from the OSeMOSYS model is provided in the `dashboard` folder. Instructions for its installation and how to run it are presented below.

## Installation instructions:

1.	You should have installed a distribution of python 3.x in your computer. 
2.	If you are using the Anaconda distribution of Python, install all python packages required listed in the `requirements.txt` file using the `conda install -c conda-forge --file requirements.txt` command in your computer bash or anaconda prompt. Alternatively, you can create a virtual environment using venv and install all required packages there using pip:
```
cd <path-to-the-dashboard-folder>
pip install virtualenv
virtualenv -p python venv
source venv/Scripts/activate
pip install -r requirements.txt
``` 
## Running the dashboard:
After installing all required packages, the dashboard can be run locally by running `python app.py` in your bash or anaconda prompt. A local host URL will be displayed as: http://127.0.0.1:8050/ copy it and paste it in your browser.

To exit the app, type CTRL + C a couple of times in your bash.
