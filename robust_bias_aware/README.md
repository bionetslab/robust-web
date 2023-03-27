# Installation

Install conda environment as follows (there also exists an environment.yml but it contains more packages than necessary)
```bash
conda create --name robust python=3.7
conda activate robust
conda install numpy matplotlib pandas networkx pip jupyter
pip install pcst_fast
```

# Running ROBUST

You can simply run robust by calling
```bash
python3 robust.py data/data-example1-prec-puberty/BioGRID.txt data/data-example1-prec-puberty/prec-pub-seeds.txt prec_puberty.graphml
```
The positional arguments are:
```

[1] file with a list of seed genes (delimiter: newline-separated)
[2] path to output file (supported output file types: .graphml, .csv, others) [read more below]


The suffix of the path to the output file you specify, determine the format of the output.
You can either choose
- .graphml: A .graphml file is written that contains the following vertex properties: isSeed, significance, nrOfOccurrences, connected_components_id, trees
- .csv: A .csv file which contains a vertex table with #occurrences, %occurrences, terminal (isSeed) 
- everything else: An edge list

```
The optional arguments are:
```

[1] --network NETWORK					Description: Specify path to graph or identifier of networks shipped with ROBUST ('BioGRID', 'APID', 'STRING'), type=str or file (allowed types: .graphml, .txt, .csv, .tsv), default: 'BioGRID' [read more below]

Network input options:
	- A two-column edgelist. File types and corresponding delimiters are as follows: 1. '.txt' file should be space-separated 2. '.tsv' file should be tab-separated 3. '.csv' file should be comma-separated. No other file  formats except '.txt', '.csv' and '.tsv' are accepted at the moment.
	- A valid .graphml file
	- In-built network name {'BioGRID', 'APID', 'STRING'}


[2] --alpha ALPHA					Description: initial fraction for ROBUST, type=float, expected range=[0,1], default: 0.25

[3] --beta BETA						Description: reduction factor for ROBUST, type=float, expected range=[0,1], default: 0.90

[4] --n N						Description: # of steiner trees for ROBUST, type=int, expected range=(0,+inf], default: 30

[5] --tau TAU						Description: threshold value for ROBUST, type=float, expected range=(0,+inf], default: 0.1

[6] --namespace {'ENTREZ', 'GENE_SYMBOL', 'UNIPROT', 'ENSEMBL'}	Description: gene/ protein identifier options for study bias data, type=str, default: 'GENE_SYMBOL'

[7] --study-bias-scores					Description: specify edge weight function used by ROBUST, type=str, default: 'BAIT_USAGE' [read more below]

Study bias score input options:
	- A two-column file (delimiter: comma), where the first column is the gene or protein name (column datatype: string) and the second column is the study bias score (column datatype: int).
	- In-built study-bias-score options {'NONE' or 'None', 'BAIT_USAGE', 'STUDY_ATTENTION'} ('NONE' or 'None' leads to running ROBUST with uniform edge costs.)


--gamma							Description: Hyper-parameter gamma used by bias-aware edge weights. This hyperparameter regulates to what extent the study bias data is being leveraged when running ROBUST., type=float, expected range=[0,1], default: 1.00
```

# Updating in-built PPI networks
```bash
python3 ./data/networks/update_inbuilt_ppi_networks.py
```

# Updating study bias scores
```bash
python3 ./data/study_bias_scores/update_inbuilt_study_bias_scores.py
```


# Evaluating ROBUST

For a large-scale empirical evaluation of ROBUST, please follow the instructions given here: https://github.com/bionetslab/robust-eval.

# Citing ROBUST

Please cite ROBUST as follows:
- **citation will be added once available**
