MODELRUNS = ['bau', 'currentpolicies', 'sdg7']

rule all:
	input: ["results/{modelrun}/csv/AccumulatedNewCapacity.csv".format(modelrun=x) for x in MODELRUNS]
	message: "Running pipeline to generate the files '{input}'"

rule prepare_model:
	output: "processed_data/{modelrun}/osemosys.txt"
	params: modelrun="{modelrun}"
	shell:
		"bash scripts/osemosys_run.sh {params.modelrun}"

rule solve:
	input: data="data/data_{modelrun}.txt", model="processed_data/{modelrun}/osemosys.txt"
	output: results="results/{modelrun}.sol",csv="results/{modelrun}/csv/AccumulatedNewCapacity.csv"
	log: "processed_data/{modelrun}/glpsol.log"
	conda: "env/osemosys.yaml"
	shell:
		"glpsol -d {input.data} -m {input.model} -o {output.results} > {log}"

rule clean:
	shell:
		"rm -f processed_data/*/*.pdf processed_data/*/*.sol processed_data/*/*.csv *.png"

rule make_dag:
	output: pipe("dag.txt")
	shell:
		"snakemake --dag > {output}"

rule plot_dag:
	input: "dag.txt"
	output: "dag.png"
	conda: "env/dag.yaml"
	shell:
		"dot -Tpng {input} > dag.png && open dag.png"