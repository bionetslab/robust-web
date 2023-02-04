import networkx as nx
import pandas as pd
# robust_dev_branch_clean/data/study_bias_scores/UNIPROT_STUDY_ATTENTION.csv

def add_study_bias_scores_to_network(path_to_study_bias_scores: str, network: nx.Graph):
    """
    Reads the PPI-graph from file without any attributes such as weight.
    """
    study_bias_scores = pd.read_csv(path_to_study_bias_scores)
    # print(study_bias_scores)
    study_bias_dict = { study_bias_scores.loc[i, 'gene_or_protein']: study_bias_scores.loc[i, 'study_bias_score'] for i in range(study_bias_scores.shape[0]) }
    # study_bias_dict=study_bias_scores.to_dict('list')
    # study_bias_dict = dict(zip(study_bias_scores.gene_or_protein, study_bias_scores.study_bias_score))
    nx.set_node_attributes(network, 1, 'study_bias_score')
    for node in network:
        network.nodes[node]['study_bias_score'] = study_bias_dict.get(node, 1)


def read_ppi_network(network: str, flag):
    """
    Reads the PPI-graph from file without any attributes such as weight.
    """
    if flag==1:
        return network
    else:
        vertices = set()
        edges = []
        with open(network, "r") as file:
            file.readline()
            for line in file:
                if network.endswith('.tsv'):
                    parsed_line = line.split('\t')
                elif network.endswith('.csv'):
                    parsed_line = line.split(',')
                elif network.endswith('.txt'):
                    parsed_line = line.split(' ')
                v = parsed_line[0].strip()
                w = parsed_line[1].strip()
                vertices.add(v)
                vertices.add(w)
                edges.append((v,w))
        network = nx.Graph()
        for v in vertices:
            network.add_node(v, label=str(v))
        network.add_edges_from(edges)
    return network
