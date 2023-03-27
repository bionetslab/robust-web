import json
import ndex2
import networkx as nx
import pandas as pd
import mygene
from update_networks import update_networks

from pybiomart import Server

server = Server(host='http://www.ensembl.org')

dataset = (server.marts['ENSEMBL_MART_ENSEMBL']
                 .datasets['hsapiens_gene_ensembl'])

ensembl_geneName_df=dataset.query(attributes=['ensembl_gene_id', 'external_gene_name'],
              filters={'chromosome_name': ['1','2']})

geneName_ensembl_dict=dict(zip(ensembl_geneName_df['Gene name'], ensembl_geneName_df['Gene stable ID']))

# update_networks(geneName_ensembl_dict)

update_networks()