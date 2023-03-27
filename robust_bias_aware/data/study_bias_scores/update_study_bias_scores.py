import requests, zipfile, io
import pandas as pd
import numpy as np
import mygene


def update_study_bias_scores(geneName_ensembl_dict):

    #########################*****************************************************************************************************#########################
    ######################################################## Data downloading code: ########################################################
    #########################*****************************************************************************************************#########################

    # # #url = "http://ftp.ebi.ac.uk/pub/databases/intact/2021-10-13/psimitab/intact.zip"
    # url = "http://ftp.ebi.ac.uk/pub/databases/intact/current/psimitab/intact.zip"

    # # print('Downloading...')
    # r = requests.get(url)
    # z = zipfile.ZipFile(io.BytesIO(r.content))
    # z.extractall(".")


    # # # read the intact file
    # intact = pd.read_table('intact.txt')

    # # modify the name of the first column
    # intact.columns.values[0] = 'ID(s) interactor A'

    # #### select only human interactions
    # intact_human = intact[((intact['Taxid interactor A'] == 'taxid:9606(human)|taxid:9606(Homo sapiens)') & (intact['Taxid interactor B'] == 'taxid:9606(human)|taxid:9606(Homo sapiens)'))]
    # intact_human['Taxid interactor A'].unique()
    # intact_human['Taxid interactor B'].unique()

    # # select only proteins
    # intact_human = intact_human[((intact_human['Type(s) interactor A'] == 'psi-mi:"MI:0326"(protein)') & (intact_human['Type(s) interactor B'] == 'psi-mi:"MI:0326"(protein)'))]

    # # retain rows with only uniprot ID
    # intact_human = intact_human[intact_human['ID(s) interactor A'].str.contains('uniprotkb') == True]
    # intact_human = intact_human[intact_human['ID(s) interactor B'].str.contains('uniprotkb') == True]

    # # eliminate 'uniprotkb:' from the first two columns
    # intact_human['ID(s) interactor A'] = intact_human['ID(s) interactor A'].replace('uniprotkb:','',regex = True)
    # intact_human['ID(s) interactor B'] = intact_human['ID(s) interactor B'].replace('uniprotkb:','',regex = True)

    # # retrieve only the role in the parenthesis
    # intact_human['Experimental role(s) interactor A'] = intact_human['Experimental role(s) interactor A'].apply(lambda st: st[st.find("(")+1:st.find(")")])
    # intact_human['Experimental role(s) interactor B'] = intact_human['Experimental role(s) interactor B'].apply(lambda st: st[st.find("(")+1:st.find(")")])

    # # eliminate -1 from the name of the uniprot ID
    # intact_human['ID(s) interactor A'] = intact_human['ID(s) interactor A'].replace('-1','',regex = True)
    # intact_human['ID(s) interactor B'] = intact_human['ID(s) interactor B'].replace('-1','',regex = True)

    # # retrieve the original protein from the isoform
    # intact_human['ID(s) interactor A'] = intact_human['ID(s) interactor A'].str.split('-').str[0]
    # intact_human['ID(s) interactor B'] = intact_human['ID(s) interactor B'].str.split('-').str[0]

    # # retrieve only the pubmed ID
    # intact_human['Publication Identifier(s)'] = intact_human['Publication Identifier(s)'].str.extract(r'(pubmed:\w+)')
    # intact_human['Publication Identifier(s)'] = intact_human['Publication Identifier(s)'].replace('pubmed:','',regex = True)


    # intact_human.to_csv('intact_human.txt',index = None, sep = '\t', mode = 'w')
    # # print('Downloading Done!')

    #########################*****************************************************************************************************#########################
    ######################################################## Bait usage generation code: ########################################################
    #########################*****************************************************************************************************#########################

    # intact_human = pd.read_table('intact_human.txt', low_memory=False)
    # # print(len(intact_human))

    # # intact_human_unique = pd.DataFrame(intact_human,columns = ['ID(s) interactor A','ID(s) interactor B'])
    # # len(intact_human_unique.drop_duplicates())
    # # print(intact_human.columns)


    # bait_a = intact_human.loc[intact_human['Experimental role(s) interactor A'] == 'bait','ID(s) interactor A']
    # bait_b = intact_human.loc[intact_human['Experimental role(s) interactor B'] == 'bait','ID(s) interactor B']
    # bait = np.union1d(bait_a,bait_b)
    # # len(bait)

    # bait_usage = []
    # bait_uniprot = []
    # bait_symbol = []

    # mg = mygene.MyGeneInfo()

    # for b in bait:
    #   # print(b)
    #   table_a = intact_human[(intact_human['Experimental role(s) interactor A'] == 'bait') & (intact_human['ID(s) interactor A'] == b)]
    #   pubmed_a = table_a['Publication Identifier(s)'].unique()
    #   #table_a['Experimental role(s) interactor A'].unique()
    #   #table_a['ID(s) interactor A'].unique()
    #   table_b = intact_human[(intact_human['Experimental role(s) interactor B'] == 'bait') & (intact_human['ID(s) interactor B'] == b)]
    #   pubmed_b = table_b['Publication Identifier(s)'].unique()
    #   pubmed = np.union1d(str(pubmed_a),str(pubmed_b)) # already unique values
    #   bait_uniprot.append(b)
    #   bait_usage.append(len(pubmed))
    #   query = mg.query(b,scopes='uniprot',species=9606,fields='symbol',returnall=True)
    #   if (len(query['hits']) == 0) :
    #     bait_symbol.append('NA')
    #   elif 'symbol' not in query['hits'][0]:
    #     bait_symbol.append('NA')
    #   else:
    #     bait_symbol.append(query['hits'][0]['symbol'])
    
    
    # final_table = pd.DataFrame(np.array([bait_uniprot,bait_symbol,bait_usage]))
    # final_table = final_table.T
    # final_table.columns = ['bait_uniprot','bait_symbol','bait_usage']

    # final_table.to_csv('bait_usage_intact.txt',index = None, sep = '\t', mode = 'w')

    # # #########################*****************************************************************************************************#########################
    # # ######################################################## Data preprocessing code (BAIT_USAGE): ########################################################
    # # #########################*****************************************************************************************************#########################

    bait_usage_data = pd.read_csv('bait_usage_intact.txt', sep='\t')

    bait_uniprot=bait_usage_data['bait_uniprot']
    bait_symbol=bait_usage_data['bait_symbol']
    bait_usage=bait_usage_data['bait_usage']

    bait_uniprot_list=bait_uniprot.to_list()
    bait_symbol_list=bait_symbol.to_list()
    bait_usage_list=bait_usage.to_list()


    # Bait usage data (with GENE_SYMBOL):
    # -----------------------------------

    LENGTH_orig=len(bait_uniprot_list)
    UniprotsForMissingGeneSymbols=[]

    bait_uniprot_list1=[]
    bait_symbol_list1=[]
    bait_usage_list1=[]
    for i in range(LENGTH_orig):
        if not(isinstance(bait_symbol_list[i], str)):
            UniprotsForMissingGeneSymbols.append(bait_uniprot_list[i])
        else:
            bait_uniprot_list1.append(bait_uniprot_list[i])
            bait_symbol_list1.append(bait_symbol_list[i])
            bait_usage_list1.append(bait_usage_list[i])


    bait_usage_data_NoMissingSymbols = pd.DataFrame([bait_uniprot_list1,bait_symbol_list1,bait_usage_list1])
    bait_usage_data_NoMissingSymbols = bait_usage_data_NoMissingSymbols.transpose()
    bait_usage_data_NoMissingSymbols.columns=['bait_uniprot','bait_symbol','bait_usage']


    all_genes = list(set(bait_usage_data_NoMissingSymbols.bait_symbol))
    gene_occurences = {gene: 0 for gene in all_genes}
    gene_bait_usage = {gene: 0 for gene in all_genes}
    for i in range(bait_usage_data_NoMissingSymbols.shape[0]):
        gene = bait_usage_data_NoMissingSymbols.loc[i, 'bait_symbol']
        gene_bait_usage[gene] += bait_usage_data_NoMissingSymbols.loc[i, 'bait_usage']
        gene_occurences[gene] += 1
    gene_bait_usages = [gene_bait_usage[gene] for gene in all_genes]
    gene_bait_usage = pd.DataFrame({'gene': all_genes, 'bait_usage': gene_bait_usages})
    gene_bait_usage.set_index('gene',inplace=True)

    duplicates = [gene for gene in all_genes if gene_occurences[gene] > 1]
    ratio_of_duplicate_gene_symbols=len(duplicates) / len(all_genes)

    gene_bait_usage.to_csv('GENE_SYMBOL/BAIT_USAGE.txt', sep=' ')



    # # Bait usage data (with UNIPROT_PROTEIN_ID):
    # # ------------------------------------------

    # gene_bait_usage = pd.DataFrame({'gene': bait_uniprot_list, 'bait_usage': bait_usage_list})
    # gene_bait_usage.set_index('gene',inplace=True)
    # gene_bait_usage.to_csv('UNIPROT/BAIT_USAGE.txt', sep=' ')


    # # Bait usage data (with ENTREZ_GENE_ID):
    # # ------------------------------------------
    # ZIP=zip(bait_uniprot_list, bait_usage_list)
    # DICT=dict(ZIP)

    # NotFoundGenes=[]
    # statuscounter=0
    # cntr=0
    # geneUniprots_withFoundEntrezIDs=[]
    # EntrezIDs_Status=np.zeros((len(bait_uniprot_list),1))
    # entrez_ids = []

    # try:
    #     mg = mygene.MyGeneInfo()
    #     out = mg.querymany(bait_uniprot_list, scopes= 'uniprot', fields='entrezgene', species='human', verbose=False)
        
    #     for line in out:
    #         try:
    #             EntrezIDs_Status[statuscounter]=1
    #             entrez_ids.append(line["entrezgene"])
    #             geneUniprots_withFoundEntrezIDs.append(bait_uniprot_list[cntr])
    #             statuscounter=statuscounter+1
    #             cntr=cntr+1
    #         except KeyError:
    #             EntrezIDs_Status[statuscounter]=0
    #             NotFoundGenes.append(bait_uniprot_list[statuscounter])
    #             statuscounter=statuscounter+1
    #             pass
    # except:
    #     pass


    # NumberOfFoundGenes=len(entrez_ids)
    # NumberOfNotFoundGenes=len(NotFoundGenes)

    # bait_uniprot_list1=[]
    # bait_entrez_list1=[]
    # bait_usage_list1=[]

    # for i in range(NumberOfFoundGenes):
    #     bait_uniprot_list1.append(geneUniprots_withFoundEntrezIDs[i])
    #     bait_entrez_list1.append(entrez_ids[i])
    #     bait_usage_list1.append(DICT[geneUniprots_withFoundEntrezIDs[i]])
        


    # gene_bait_usage = pd.DataFrame({'gene': bait_entrez_list1, 'bait_usage': bait_usage_list1})
    # gene_bait_usage.set_index('gene',inplace=True)
    # gene_bait_usage.to_csv('ENTREZ/BAIT_USAGE.txt', sep=' ')
    
    
    
    # Bait usage data (with ENSEMBL id):
    # ------------------------------------------
    ZIP=zip(bait_symbol_list, bait_usage_list)
    DICT=dict(ZIP)

    NotFoundGenes=[]
    statuscounter=0
    cntr=0
    geneUniprots_withFoundEntrezIDs=[]
    EntrezIDs_Status=np.zeros((len(bait_symbol_list),1))
    entrez_ids = []

    # try:
    #     mg = mygene.MyGeneInfo()
    #     out = mg.querymany(bait_uniprot_list, scopes= 'uniprot', fields='ensembl.gene', species='human', verbose=False)
        
    for line in bait_symbol_list:
        try:
            EntrezIDs_Status[statuscounter]=1
            entrez_ids.append(geneName_ensembl_dict[line])
            geneUniprots_withFoundEntrezIDs.append(bait_symbol_list[cntr])
            statuscounter=statuscounter+1
            cntr=cntr+1
        except:
            EntrezIDs_Status[statuscounter]=0
            NotFoundGenes.append(bait_symbol_list[statuscounter])
            statuscounter=statuscounter+1
    # except:
    #     pass


    NumberOfFoundGenes=len(entrez_ids)
    NumberOfNotFoundGenes=len(NotFoundGenes)

    bait_uniprot_list1=[]
    bait_entrez_list1=[]
    bait_usage_list1=[]

    for i in range(NumberOfFoundGenes):
        bait_uniprot_list1.append(geneUniprots_withFoundEntrezIDs[i])
        bait_entrez_list1.append(entrez_ids[i])
        bait_usage_list1.append(DICT[geneUniprots_withFoundEntrezIDs[i]])
        


    # gene_bait_usage = pd.DataFrame({'gene': bait_entrez_list1, 'bait_usage': bait_usage_list1})
    # gene_bait_usage.set_index('gene',inplace=True)
    gene_bait_usage = pd.DataFrame({'gene_or_protein': bait_entrez_list1, 'study_bias_score': bait_usage_list1})
    gene_bait_usage.set_index('gene_or_protein',inplace=True)
    # gene_bait_usage.to_csv('ENSEMBL/BAIT_USAGE.txt', sep=' ')
    gene_bait_usage.to_csv('ENSEMBL/BAIT_USAGE.csv')


    # # # #########################*****************************************************************************************************#########################
    # # ################################################################# Data preprocessing code (STUDY_ATTENTION): #################################################################
    # # # #########################*****************************************************************************************************#########################

    PAIR_FREQ_DATA=pd.read_csv('pair_study_frequency.txt', sep = ' ')

    IDs_interactor_A=PAIR_FREQ_DATA['IDs_interactor_A']
    IDs_interactor_B=PAIR_FREQ_DATA['IDs_interactor_B']
    freq=PAIR_FREQ_DATA['freq']
    symbol_A=PAIR_FREQ_DATA['symbol_A']
    symbol_B=PAIR_FREQ_DATA['symbol_B']

    IDs_interactor_A=IDs_interactor_A.to_list()
    IDs_interactor_B=IDs_interactor_B.to_list()
    freq=freq.to_list()
    symbol_A=symbol_A.to_list()
    symbol_B=symbol_B.to_list()

    # Study attention data (with GENE_SYMBOL):
    # ----------------------------------------

    LENGTH_orig=len(freq)

    list_status_A=np.ones((LENGTH_orig,1))
    list_status_B=np.ones((LENGTH_orig,1))

    MissingIDs_A=[]
    MissingIDs_B=[]

    IDs_A=[]
    IDs_B=[]
    symbols_A=[]
    symbols_B=[]
    freqs=[]

    for i in range(LENGTH_orig):
        if isinstance(symbol_A[i], str) and isinstance(symbol_B[i], str):
            IDs_A.append(IDs_interactor_A[i])
            IDs_B.append(IDs_interactor_B[i])
            symbols_A.append(symbol_A[i])
            symbols_B.append(symbol_B[i])
            freqs.append(freq[i])
        else:
            if not(isinstance(symbol_A[i], str)):
                list_status_A[i]=0
                MissingIDs_A.append(IDs_interactor_A[i])
            if not(isinstance(symbol_B[i], str)):
                list_status_B[i]=0
                MissingIDs_B.append(IDs_interactor_B[i]) 
            
    noOfMissingGeneSymbols_A=len(MissingIDs_A)
    noOfMissingGeneSymbols_B=len(MissingIDs_B)


    pair_freqs_NoMissingSymbols = pd.DataFrame([IDs_A,IDs_B,freqs,symbols_A,symbols_B])
    pair_freqs_NoMissingSymbols = pair_freqs_NoMissingSymbols.transpose()
    pair_freqs_NoMissingSymbols.columns=['IDs_interactor_A','IDs_interactor_B','freq','symbol_A','symbol_B']


    all_genes = list(set(pair_freqs_NoMissingSymbols.symbol_A).union(set(pair_freqs_NoMissingSymbols.symbol_B)))
    study_attention = {gene: 0 for gene in all_genes}

    for i in range(pair_freqs_NoMissingSymbols.shape[0]):
        gene = pair_freqs_NoMissingSymbols.loc[i,'symbol_A']
        if type(gene) == str:
            study_attention[gene] += 1
        gene = pair_freqs_NoMissingSymbols.loc[i,'symbol_B']
        if type(gene) == str:
            study_attention[gene] += 1

    genes = [gene for gene, _ in study_attention.items()]
    counts = [count for _, count in study_attention.items()]
    study_att = pd.DataFrame({'gene': genes, 'study_attention': counts})
    study_att.set_index('gene', inplace=True)
    study_att.to_csv('GENE_SYMBOL/STUDY_ATTENTION.txt', sep=' ')
    
    
    
    # Study attention data (with ENSEMBL):
    # ------------------------------------

    DICT = dict(zip(study_att.index, study_att.study_attention))
    gene_=list(study_att.index)
    studyAttention_=list(study_att.study_attention)
    NotFoundGenes=[]
    statuscounter=0
    cntr=0
    geneUniprots_withFoundEntrezIDs=[]
    EntrezIDs_Status=np.zeros((len(gene_),1))
    entrez_ids = []


    for line in bait_symbol_list:
        try:
            EntrezIDs_Status[statuscounter]=1
            entrez_ids.append(geneName_ensembl_dict[line])
            geneUniprots_withFoundEntrezIDs.append(gene_[cntr])
            statuscounter=statuscounter+1
            cntr=cntr+1
        except KeyError:
            EntrezIDs_Status[statuscounter]=0
            NotFoundGenes.append(gene_[statuscounter])
            statuscounter=statuscounter+1
            pass

    NumberOfFoundGenes=len(entrez_ids)
    NumberOfNotFoundGenes=len(NotFoundGenes)

    bait_uniprot_list1=[]
    bait_entrez_list1=[]
    bait_usage_list1=[]

    for i in range(NumberOfFoundGenes):
        bait_uniprot_list1.append(geneUniprots_withFoundEntrezIDs[i])
        bait_entrez_list1.append(entrez_ids[i])
        bait_usage_list1.append(DICT[geneUniprots_withFoundEntrezIDs[i]])

    # study_att = pd.DataFrame({'gene': bait_entrez_list1, 'study_attention': bait_usage_list1})
    # study_att.set_index('gene', inplace=True)
    study_att = pd.DataFrame({'gene_or_protein': bait_entrez_list1, 'study_bias_score': bait_usage_list1})
    study_att.set_index('gene_or_protein', inplace=True)
    # study_att.to_csv('ENSEMBL/STUDY_ATTENTION.txt', sep=' ')
    study_att.to_csv('ENSEMBL/STUDY_ATTENTION.csv')
    

    # # Study attention data (with UNIPROT_PROTEIN_ID and ENTREZ_GENE_ID):
    # # ------------------------------------------------------------------

    # # uniprot_protein_ids:

    # all_genes = list(set(PAIR_FREQ_DATA.IDs_interactor_A).union(set(PAIR_FREQ_DATA.IDs_interactor_B)))
    # study_attention = {gene: 0 for gene in all_genes}

    # for i in range(PAIR_FREQ_DATA.shape[0]):
    #     gene = PAIR_FREQ_DATA.loc[i,'IDs_interactor_A']
    #     if type(gene) == str:
    #         study_attention[gene] += 1
    #     gene = PAIR_FREQ_DATA.loc[i,'IDs_interactor_B']
    #     if type(gene) == str:
    #         study_attention[gene] += 1

    # genes = [gene for gene, _ in study_attention.items()]
    # counts = [count for _, count in study_attention.items()]
    # study_att = pd.DataFrame({'gene': genes, 'study_attention': counts})
    # studyAtt_=pd.DataFrame({'gene': genes, 'study_attention': counts})
    # study_att.set_index('gene', inplace=True)
    # study_att.to_csv('UNIPROT/STUDY_ATTENTION.txt', sep=' ')


    # # entrez_gene_ids:

    # DICT = dict(zip(studyAtt_.gene, studyAtt_.study_attention))
    # gene_=list(studyAtt_.gene)
    # studyAttention_=list(studyAtt_.study_attention)
    # NotFoundGenes=[]
    # statuscounter=0
    # cntr=0
    # geneUniprots_withFoundEntrezIDs=[]
    # EntrezIDs_Status=np.zeros((len(gene_),1))
    # entrez_ids = []


    # try:
    #     mg = mygene.MyGeneInfo()
    #     out = mg.querymany(gene_, scopes= 'uniprot', fields='entrezgene', species='human', verbose=False)
        
    #     for line in out:
    #         try:
    #             EntrezIDs_Status[statuscounter]=1
    #             entrez_ids.append(line["entrezgene"])
    #             geneUniprots_withFoundEntrezIDs.append(gene_[cntr])
    #             statuscounter=statuscounter+1
    #             cntr=cntr+1
    #         except KeyError:
    #             EntrezIDs_Status[statuscounter]=0
    #             NotFoundGenes.append(gene_[statuscounter])
    #             statuscounter=statuscounter+1
    #             pass
    # except:
    #     pass


    # NumberOfFoundGenes=len(entrez_ids)
    # NumberOfNotFoundGenes=len(NotFoundGenes)

    # bait_uniprot_list1=[]
    # bait_entrez_list1=[]
    # bait_usage_list1=[]

    # for i in range(NumberOfFoundGenes):
    #     bait_uniprot_list1.append(geneUniprots_withFoundEntrezIDs[i])
    #     bait_entrez_list1.append(entrez_ids[i])
    #     bait_usage_list1.append(DICT[geneUniprots_withFoundEntrezIDs[i]])

    # study_att = pd.DataFrame({'gene': bait_entrez_list1, 'study_attention': bait_usage_list1})
    # study_att.set_index('gene', inplace=True)
    # study_att.to_csv('ENTREZ/STUDY_ATTENTION.txt', sep=' ')


    # #########################*****************************************************************************************************#########################
    # #########################################################################################################################################################
    # #########################*****************************************************************************************************#########################
