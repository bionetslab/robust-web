import json
import ndex2
import networkx as nx
import pandas as pd
import mygene
import os

def update_networks():
    client = ndex2.client.Ndex2()

    # (1.2) APID Human Interactome (only human proteins):
    APID = client.get_network_as_cx_stream('9c38ce6e-c564-11e8-aaa6-0ac135e8bacf')
    APID = ndex2.create_nice_cx_from_raw_cx(json.loads(APID.content))
    APID = APID.to_networkx(mode='default')

    # (2) BioGRID:
    BioGRID = client.get_network_as_cx_stream('becec556-86d4-11e7-a10d-0ac135e8bacf')
    BioGRID = ndex2.create_nice_cx_from_raw_cx(json.loads(BioGRID.content))
    BioGRID = BioGRID.to_networkx(mode='default')

    # # 'STRING' often throws network errors (especially at line 'ndex2.create_nice_cx_from_raw_cx')-this is an ndex server issue.
    # # That is why this dataset has been run in try-catch blocks of upto 3 failed attempts.
    # # If still not updated, will be updated in next scheduled cycle:

    # (4) STRING:
    count=0
    status=0
    while count<3:
        try:
            STRING = client.get_network_as_cx_stream('275bd84e-3d18-11e8-a935-0ac135e8bacf')
            STRING = ndex2.create_nice_cx_from_raw_cx(json.loads(STRING.content))
            STRING = STRING.to_networkx(mode='default')
            status=1
        except:
            pass
        if status==1:
            break

    ####################################################################### APID: #######################################################################

    src=[]
    dest=[]
    for u, v in nx.get_edge_attributes(APID,'name').items():
        nodes_=v.split(' (interacts with) ')
        src.append(nodes_[0])
        dest.append(nodes_[1])
    APID_UNIPROT = {'node1':src,'node2':dest}
    APID_UNIPROT = pd.DataFrame(APID_UNIPROT)

    outname='APID.txt'
    outdir = './UNIPROT'
    if not os.path.exists(outdir):
        os.mkdir(outdir)
    fullname = os.path.join(outdir, outname)

    APID_UNIPROT.to_csv(fullname, sep=' ', index=False)

    # ------------------------------------------------------------------------

    src_set=set(src)
    dest_set=set(dest)
    nodes_set=src_set.union(dest_set)
    nodes_=list(nodes_set)

    try:
        mg = mygene.MyGeneInfo()
        # out = mg.querymany(nodes_, scopes= 'symbol', fields='entrezgene', species='human', verbose=False)
        out = mg.querymany(nodes_, scopes= 'uniprot', fields='symbol', species='human', verbose=False)
    except:
        pass

    NODES_uniprot=[]
    NODES_genesymbol=[]
    for i in range(len(out)):
        try:
            NODES_genesymbol.append(out[i]['symbol'])
            NODES_uniprot.append(out[i]['query'])
        except:
            pass

    uniprot_genesymbol_DICT=dict(zip(NODES_uniprot, NODES_genesymbol))

    SRC=[]
    DEST=[]

    for i in src:
        try:
            SRC.append(uniprot_genesymbol_DICT[i])
        except:
            SRC.append(i)

    for i in dest:
        try:
            DEST.append(uniprot_genesymbol_DICT[i])
        except:
            DEST.append(i)

    APID_GENE_SYMBOL={'node1':SRC,'node2':DEST}
    APID_GENE_SYMBOL = pd.DataFrame(APID_GENE_SYMBOL)

    outname='APID.txt'
    outdir = './GENE_SYMBOL'
    if not os.path.exists(outdir):
        os.mkdir(outdir)
    fullname = os.path.join(outdir, outname)

    APID_GENE_SYMBOL.to_csv(fullname, sep=' ', index=False)

    # ----------------------------------------------------------------------

    src_set=set(src)
    dest_set=set(dest)
    nodes_set=src_set.union(dest_set)
    nodes_=list(nodes_set)

    try:
        mg = mygene.MyGeneInfo()
        out = mg.querymany(nodes_, scopes= 'uniprot', fields='entrezgene', species='human', verbose=False)
    except:
        pass


    NODES_uniprot=[]
    NODES_entrezgene=[]
    for i in range(len(out)):
        try:
            NODES_entrezgene.append(out[i]['entrezgene'])
            NODES_uniprot.append(out[i]['query'])
        except:
            pass

    uniprot_entrezgene_DICT=dict(zip(NODES_uniprot, NODES_entrezgene))

    SRC=[]
    DEST=[]

    for i in src:
        try:
            SRC.append(uniprot_entrezgene_DICT[i])
        except:
            SRC.append(i)

    for i in dest:
        try:
            DEST.append(uniprot_entrezgene_DICT[i])
        except:
            DEST.append(i)

    APID_ENTREZGENE={'node1':SRC,'node2':DEST}
    APID_ENTREZGENE = pd.DataFrame(APID_ENTREZGENE)

    outname='APID.txt'
    outdir = './ENTREZ'
    if not os.path.exists(outdir):
        os.mkdir(outdir)
    fullname = os.path.join(outdir, outname)
    

    APID_ENTREZGENE.to_csv(fullname, sep=' ', index=False)

    # ####################################################################### BIOGRID: #######################################################################

    nodes_=[]
    node_attributes=[]
    for u, v in nx.get_node_attributes(BioGRID,'represents').items():
        symbols_=v.split('hgnc.symbol:')
        symbol=symbols_[1]
        nodes_.append(u)
        node_attributes.append(symbol)
    nodes_attributes_DICT=dict(zip(nodes_, node_attributes))

    edges_=BioGRID.edges
    edges_list=list(edges_)
    LIST=list(map(list, zip(*edges_list)))

    src=[]
    dest=[]
    for i in LIST[0]:
        src.append(nodes_attributes_DICT[i])
    for i in LIST[1]:
        dest.append(nodes_attributes_DICT[i])

    BioGRID_GENE_SYMBOL={'node1':src,'node2':dest}
    BioGRID_GENE_SYMBOL = pd.DataFrame(BioGRID_GENE_SYMBOL)

    outname='BioGRID.txt'
    outdir = './GENE_SYMBOL'
    if not os.path.exists(outdir):
        os.mkdir(outdir)
    fullname = os.path.join(outdir, outname)

    BioGRID_GENE_SYMBOL.to_csv(fullname, sep=' ', index=False)

    # ----------------------------------------------------------------------

    src_set=set(src)
    dest_set=set(dest)
    nodes_set=src_set.union(dest_set)
    nodes_=list(nodes_set)

    try:
        mg = mygene.MyGeneInfo()
        # out = mg.querymany(nodes_, scopes= 'symbol', fields='entrezgene', species='human', verbose=False)
        out = mg.querymany(nodes_, scopes= 'symbol', fields='uniprot', species='human', verbose=False)
    except:
        pass

    nodes_genesymbol=[]
    nodes_uniprot=[]
    for i in range(len(out)):
        try:
            nodes_uniprot.append(out[i]['uniprot'])
            nodes_genesymbol.append(out[i]['query'])
        except:
            pass

    NODES_genesymbol=[]

    NODES_uniprot=[]

    for i in range(len(nodes_uniprot)):
        try:
            NODES_uniprot.append(nodes_uniprot[i]['Swiss-Prot'])
            NODES_genesymbol.append(nodes_genesymbol[i])
        except:
            pass

    genesymbol_uniprot_DICT=dict(zip(NODES_genesymbol, NODES_uniprot))

    SRC=[]
    DEST=[]

    for i in src:
        try:
            SRC.append(genesymbol_uniprot_DICT[i])
        except:
            SRC.append(i)

    for i in dest:
        try:
            DEST.append(genesymbol_uniprot_DICT[i])
        except:
            DEST.append(i)

    BioGRID_UNIPROT={'node1':SRC,'node2':DEST}
    BioGRID_UNIPROT = pd.DataFrame(BioGRID_UNIPROT)

    outname='BioGRID.txt'
    outdir = './UNIPROT'
    if not os.path.exists(outdir):
        os.mkdir(outdir)
    fullname = os.path.join(outdir, outname)

    BioGRID_UNIPROT.to_csv(fullname, sep=' ', index=False)

    # ----------------------------------------------------------------------

    src_set=set(src)
    dest_set=set(dest)
    nodes_set=src_set.union(dest_set)
    nodes_=list(nodes_set)

    try:
        mg = mygene.MyGeneInfo()
        out = mg.querymany(nodes_, scopes= 'symbol', fields='entrezgene', species='human', verbose=False)
    except:
        pass


    NODES_genesymbol=[]
    NODES_entrezgene=[]
    for i in range(len(out)):
        try:
            NODES_entrezgene.append(out[i]['entrezgene'])
            NODES_genesymbol.append(out[i]['query'])
        except:
            pass

    genesymbol_entrezgene_DICT=dict(zip(NODES_genesymbol, NODES_entrezgene))

    SRC=[]
    DEST=[]

    for i in src:
        try:
            SRC.append(genesymbol_entrezgene_DICT[i])
        except:
            SRC.append(i)

    for i in dest:
        try:
            DEST.append(genesymbol_entrezgene_DICT[i])
        except:
            DEST.append(i)

    BioGRID_ENTREZGENE={'node1':SRC,'node2':DEST}
    BioGRID_ENTREZGENE = pd.DataFrame(BioGRID_ENTREZGENE)

    outname='BioGRID.txt'
    outdir = './ENTREZ'
    if not os.path.exists(outdir):
        os.mkdir(outdir)
    fullname = os.path.join(outdir, outname)

    BioGRID_ENTREZGENE.to_csv(fullname, sep=' ', index=False)

    ####################################################################### STRING: #######################################################################

    nodes_=[]
    node_attributes=[]
    for u, v in nx.get_node_attributes(STRING,'represents').items():
        symbols_=v.split('hgnc.symbol:')
        symbol=symbols_[1]
        nodes_.append(u)
        node_attributes.append(symbol)
    nodes_attributes_DICT=dict(zip(nodes_, node_attributes))

    edges_=STRING.edges
    edges_list=list(edges_)
    LIST=list(map(list, zip(*edges_list)))

    src=[]
    dest=[]
    for i in LIST[0]:
        src.append(nodes_attributes_DICT[i])
    for i in LIST[1]:
        dest.append(nodes_attributes_DICT[i])

    STRING_GENE_SYMBOL={'node1':src,'node2':dest}
    STRING_GENE_SYMBOL = pd.DataFrame(STRING_GENE_SYMBOL)

    outname='STRING.txt'
    outdir = './GENE_SYMBOL'
    if not os.path.exists(outdir):
        os.mkdir(outdir)
    fullname = os.path.join(outdir, outname)

    STRING_GENE_SYMBOL.to_csv(fullname, sep=' ', index=False)

    # ----------------------------------------------------------------------

    src_set=set(src)
    dest_set=set(dest)
    nodes_set=src_set.union(dest_set)
    nodes_=list(nodes_set)

    try:
        mg = mygene.MyGeneInfo()
        # out = mg.querymany(nodes_, scopes= 'symbol', fields='entrezgene', species='human', verbose=False)
        out = mg.querymany(nodes_, scopes= 'symbol', fields='uniprot', species='human', verbose=False)
    except:
        pass

    nodes_genesymbol=[]
    nodes_uniprot=[]
    for i in range(len(out)):
        try:
            nodes_uniprot.append(out[i]['uniprot'])
            nodes_genesymbol.append(out[i]['query'])
        except:
            pass

    NODES_genesymbol=[]

    NODES_uniprot=[]

    for i in range(len(nodes_uniprot)):
        try:
            NODES_uniprot.append(nodes_uniprot[i]['Swiss-Prot'])
            NODES_genesymbol.append(nodes_genesymbol[i])
        except:
            pass

    genesymbol_uniprot_DICT=dict(zip(NODES_genesymbol, NODES_uniprot))

    SRC=[]
    DEST=[]

    for i in src:
        try:
            SRC.append(genesymbol_uniprot_DICT[i])
        except:
            SRC.append(i)

    for i in dest:
        try:
            DEST.append(genesymbol_uniprot_DICT[i])
        except:
            DEST.append(i)

    STRING_UNIPROT={'node1':SRC,'node2':DEST}
    STRING_UNIPROT = pd.DataFrame(STRING_UNIPROT)

    outname='STRING.txt'
    outdir = './UNIPROT'
    if not os.path.exists(outdir):
        os.mkdir(outdir)
    fullname = os.path.join(outdir, outname)

    STRING_UNIPROT.to_csv(fullname, sep=' ', index=False)

    # ----------------------------------------------------------------------

    src_set=set(src)
    dest_set=set(dest)
    nodes_set=src_set.union(dest_set)
    nodes_=list(nodes_set)

    try:
        mg = mygene.MyGeneInfo()
        out = mg.querymany(nodes_, scopes= 'symbol', fields='entrezgene', species='human', verbose=False)
    except:
        pass


    NODES_genesymbol=[]
    NODES_entrezgene=[]
    for i in range(len(out)):
        try:
            NODES_entrezgene.append(out[i]['entrezgene'])
            NODES_genesymbol.append(out[i]['query'])
        except:
            pass

    genesymbol_entrezgene_DICT=dict(zip(NODES_genesymbol, NODES_entrezgene))

    SRC=[]
    DEST=[]

    for i in src:
        try:
            SRC.append(genesymbol_entrezgene_DICT[i])
        except:
            SRC.append(i)

    for i in dest:
        try:
            DEST.append(genesymbol_entrezgene_DICT[i])
        except:
            DEST.append(i)

    STRING_ENTREZGENE={'node1':SRC,'node2':DEST}
    STRING_ENTREZGENE = pd.DataFrame(STRING_ENTREZGENE)

    outname='STRING.txt'
    outdir = './ENTREZ'
    if not os.path.exists(outdir):
        os.mkdir(outdir)
    fullname = os.path.join(outdir, outname)

    STRING_ENTREZGENE.to_csv(fullname, sep=' ', index=False)