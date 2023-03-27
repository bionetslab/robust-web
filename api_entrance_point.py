import sys
import argparse
import json
import networkx as nx
from networkx.readwrite import json_graph
from robust_bias_aware.robust.main import run 
import requests, zipfile, io
import pandas as pd
import numpy as np
import mygene
import time

def api_entrance_point(input_array):
    node_list, api_output_df, is_seed, robust_run_time=check_input(input_array)
    return node_list, api_output_df, is_seed, robust_run_time

def check_input(input_array):
    seeds, network, namespace, alpha, beta, n, tau, gamma, study_bias_score, in_built_network, is_graphml=_initialize_params(input_array)
    study_bias_score=_process_study_bias_score_contents(study_bias_score, input_array)
    outfile=_set_default_outfile_value()
    provided_network=_process_input_network_contents(in_built_network, is_graphml, input_array)
    n -=1
    t0 = time.time()
    robust_output_df, robust_output_subgraph=run(seeds, provided_network, namespace, alpha, beta, n, tau, study_bias_score, gamma, outfile)
    t1 = time.time()
    robust_run_time = t1-t0
    # Let's call robust_output_subgraph 'G' for easier programming:
    G=robust_output_subgraph
    node_list, is_seed=preprocess_node_data_in_robust_output_subnetwork(G)
    output_data_df=preprocess_edge_data_in_robust_output_subnetwork(G)
    return node_list, output_data_df, is_seed, robust_run_time

def _initialize_params(input_array):
    seeds=str(input_array["seeds"])
    seeds = seeds.split()
    network=str(input_array["path_to_graph"])
    namespace=input_array["namespace"]
    alpha=input_array["alpha"]
    beta=input_array["beta"]
    n=input_array["n"]
    tau=input_array["tau"]
    gamma= input_array["gamma"]
    study_bias_score=input_array["study_bias_score"]
    in_built_network=input_array["in_built_network"]
    is_graphml=input_array["is_graphml"]
    return seeds, network, namespace, alpha, beta, n, tau, gamma, study_bias_score, in_built_network, is_graphml

def _process_study_bias_score_contents(study_bias_score, input_array):
    if study_bias_score=='No':
        study_bias_score='None'
    if study_bias_score=='CUSTOM':
        study_bias_score=input_array["study_bias_score_data"]
        study_bias_score = list(map(lambda x: x.split(' '),study_bias_score.split("\r\n")))
        study_bias_score=pd.DataFrame(study_bias_score[1:], columns=study_bias_score[0])
        study_bias_score.columns.values[0] = "gene_or_protein"
        study_bias_score.columns.values[1] = "study_bias_score"
    return study_bias_score

def _set_default_outfile_value():
    outfile=None
    return outfile

def _process_input_network_contents(in_built_network, is_graphml, input_array):
    if in_built_network=="No":
        if is_graphml==False:
            provided_network=input_array["provided_network"]
            provided_network = list(map(lambda x: x.split(' '),provided_network.split("\r\n")))
            provided_network=pd.DataFrame(provided_network[1:], columns=provided_network[0])
        elif is_graphml==True:
            provided_network=nx.parse_graphml(input_array["provided_network"])
    elif in_built_network=="Yes":
        provided_network=input_array["provided_network"]
    return provided_network

def preprocess_node_data_in_robust_output_subnetwork(G):
    node_list=[]
    is_seed=[]
    for i, data in G.nodes(data=True):
        node_list.append(i)
        if data['isSeed']:
            is_seed.append(int(1))
        else:
            is_seed.append(int(0))
    return node_list, is_seed

def preprocess_edge_data_in_robust_output_subnetwork(G):
    _edges=list(G.edges)
    edge_list_src=[]
    edge_list_dest=[]
    edge_data=[]
    for i,j in _edges:
        edge_list_src.append(i)
        edge_list_dest.append(j)
        edge_dict = {"from": i, "to": j, "group": "default"}
        edge_data.append(edge_dict)
    output_data_df=pd.DataFrame()
    output_data_df['edge_list_src'] = pd.Series(edge_list_src)
    output_data_df['edge_list_dest'] = pd.Series(edge_list_dest)
    return output_data_df