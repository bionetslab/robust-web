# Installation

Install conda environment as follows (there also exists a environment.yml but it contains more packages than necessary)
```bash
conda create --name biosteiner python=3.7
conda activate biosteiner
conda install numpy matplotlib pandas networkx pip jupyter
pip install pcst_fast
```

# Running ROBUST-2.00

You can simply run robust-2.00 by calling
```bash
python robust.py data/human_annotated_PPIs_brain.txt data/ms_seeds.txt ms.graphml
```
The positional arguments are:
```
[1] file providing the network in the form of an edgelist 
    (tab-separated table, columns 1 & 2 will be used)
[2] file with the seed genes (if table contains more than 
    one column they must be tab-separated; the first column 
    will be used only)
[3] path to output file
```

The optional arguments are:
```
--initial_fraction INITIAL_FRACTION							Description: initial fraction for ROBUST, type=float, expected range=[0,1], default: 0.25
--reduction_factor REDUCTION_FACTOR							Description: reduction factor for ROBUST, type=float, expected range=[0,1], default: 0.90
--number_of_steiner_trees NO_OF_STEINER_TREES						Description: # of steiner trees for ROBUST, type=int, expected range=(0,+inf], default: 30
--threshold THRESHOLD									Description: threshold value for ROBUST, type=float, expected range=(0,+inf], default: 0.1
--node_namespace {'ENTREZ_GENE_ID', 'GENE_SYMBOL', 'UNIPROT_PROTEIN_ID'}		Description: gene/ protein identifier options for study bias data, type=str, default: 'GENE_SYMBOL'
--edge_cost {'UNIFORM', 'ADDITIVE', 'EXPONENTIAL'}					Description: function for calculating edge costs, type=str, default: UNIFORM
--normalize {'BAIT_USAGE', 'STUDY_ATTENTION', 'CUSTOM'}					Description: study bias data options to be used for normalization, type=str, default: 'BAIT_USAGE'
--lambda										Description: lambda value for ROBUST-version-2.00, type=float, expected range=[0,1], default: 0.50
```

The suffix of the path to the output file you specify, determine the format of the output.
You can either choose
- .graphml: A .graphml file is written that contains the following vertex properties: isSeed, significance, nrOfOccurrences, connected_components_id, trees
- .csv: A .csv file which contains a vertex table with #occurrences, %occurrences, terminal (isSeed) 
- everything else: An edge list

# Evaluating ROBUST-2.00

For a large-scale empirical evaluation of ROBUST-2.00, please follow the instructions given here: https://github.com/bionetslab/robust-eval.

# Citing ROBUST-2.00

Please cite ROBUST-2.00 as follows:
- J. Bernett, D. Krupke, S. Sadegh1, J. Baumbach, S. P. Fekete, T. Kacprowski, M. List1, D. B. Blumenthal: Robust disease module mining via enumeration of diverse prize-collecting Steiner trees, *Bioinformatics* 38(6), pp. 1600-1606, https://doi.org/10.1093/bioinformatics/btab876.
