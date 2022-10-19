from api_entrance_point import api_entrance_point
from robust_bias_aware.data.study_bias_scores.update_study_bias_scores import update_study_bias_scores
from robust_bias_aware.data.networks.update_networks import update_networks
import flask
from flask import Flask, render_template, request
from celery import Celery
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
import json
import shortuuid
from flask_apscheduler import APScheduler

app = Flask(__name__)
app.config["CELERY_BROKER_URL"] = "redis://localhost:6379"
celery = Celery(app.name, broker=app.config["CELERY_BROKER_URL"])
celery.conf.update(app.config)


@celery.task()
def celery_running_task(custom_id, input_dict):
    node_list, api_output_df, is_seed = api_entrance_point(input_dict)
    nodeData = node_list
    edgeDataSrc = api_output_df['edge_list_src'].values.tolist()
    edgeDataDest = api_output_df['edge_list_dest'].values.tolist()
    nodeData_str = _convert_list_to_comma_separated_string(nodeData)
    edgeDataSrc_str = _convert_list_to_comma_separated_string(edgeDataSrc)
    edgeDataDest_str = _convert_list_to_comma_separated_string(edgeDataDest)
    is_seed_strings = [str(x) for x in is_seed]
    is_seed_str = ','.join(is_seed_strings)
    record = Robust(custom_id, input_dict["path_to_graph"], input_dict["seeds"], input_dict["namespace"],
                    input_dict["alpha"], input_dict["beta"], input_dict["n"], input_dict["tau"],
                    input_dict["study_bias_score"], input_dict["study_bias_score_data"], input_dict["gamma"],
                    input_dict["in_built_network"], input_dict["provided_network"], input_dict["is_graphml"],
                    nodeData_str, edgeDataSrc_str, edgeDataDest_str, is_seed_str)
    db.session.add(record)
    db.session.commit()
    return "Done!"


# Use Cron if Flask-Scheduler doesn't work well on the server:
# ------------------------------------------------------------
# cron = Scheduler(daemon=True)
# # Explicitly kick off the background thread
# cron.start()
# @cron.interval_schedule(hours=0)
# def job_function():
#     update_study_bias_data()
# # Shutdown your cron thread if the web process is stopped
# atexit.register(lambda: cron.shutdown(wait=False))

scheduler = APScheduler()


def update_study_bias_scores_scheduled_task():
    update_study_bias_scores()


def update_networks_scheduled_task():
    update_networks()


# --------------------------------------------------------------


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///robust.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'secret'

db = SQLAlchemy(app)


class Robust(db.Model):
    __tablename__ = 'robust'
    id = db.Column(db.Integer, primary_key=True)
    custom_id = db.Column(db.Integer, primary_key=False, unique=True)
    path_to_graph = db.Column(db.String)
    seeds = db.Column(db.String)
    namespace = db.Column(db.String)
    alpha = db.Column(db.Float)
    beta = db.Column(db.Float)
    n = db.Column(db.Integer, primary_key=False)
    tau = db.Column(db.Float)
    study_bias_score = db.Column(db.String)
    study_bias_score_data = db.Column(db.String)
    gamma = db.Column(db.Float)
    in_built_network = db.Column(db.String)
    provided_network = db.Column(db.String)
    is_graphml = db.Column(db.Boolean)
    nodeData_str = db.Column(db.String)
    edgeDataSrc_str = db.Column(db.String)
    edgeDataDest_str = db.Column(db.String)
    is_seed_str = db.Column(db.String)

    def __init__(self, custom_id, path_to_graph, seeds, namespace, alpha, beta, n, tau, study_bias_score,
                 study_bias_score_data, gamma, in_built_network, provided_network, is_graphml, nodeData_str,
                 edgeDataSrc_str, edgeDataDest_str, is_seed_str):
        self.custom_id = custom_id
        self.path_to_graph = path_to_graph
        self.seeds = seeds
        self.namespace = namespace
        self.alpha = alpha
        self.beta = beta
        self.n = n
        self.tau = tau
        self.study_bias_score = study_bias_score
        self.study_bias_score_data = study_bias_score_data
        self.gamma = gamma
        self.in_built_network = in_built_network
        self.provided_network = provided_network
        self.is_graphml = is_graphml
        self.nodeData_str = nodeData_str
        self.edgeDataSrc_str = edgeDataSrc_str
        self.edgeDataDest_str = edgeDataDest_str
        self.is_seed_str = is_seed_str


class Task_Added(db.Model):
    __tablename__ = 'task_added'
    id = db.Column(db.Integer, primary_key=True)
    custom_id = db.Column(db.Integer, primary_key=False, unique=True)

    def __init__(self, custom_id):
        self.custom_id = custom_id


@app.route('/', methods=['GET'])
def index():
    title_ = 'Home - ROBUST'
    return render_template('index.html', title=title_)


@app.route('/robust_about', methods=['GET'])
def robust_about():
    title_ = 'About - ROBUST'
    return render_template('robust_about.html', title=title_)


@app.route('/robust_documentation', methods=['GET'])
def robust_documentation():
    title_ = 'Documentation - ROBUST'
    return render_template('robust_documentation.html', title=title_)


@app.route('/run_robust', methods=['POST', 'GET'])
def run_robust():
    title_ = 'Run ROBUST'
    return render_template('run_robust.html', title=title_)


@app.route('/results', methods=['POST', 'GET'])
def results():
    if flask.request.method == 'POST':
        custom_id = _generate_custom_id()
        NETWORK, NAMESPACE, STUDY_BIAS_SCORE = _initialize_dropdown_params()
        study_bias_score_data = 'No'
        uploaded_network = ''
        namespace, alpha, beta, n, tau, study_bias_score, gamma, path_to_graph, uploaded_network, seeds = _initialize_input_params(
            NETWORK, NAMESPACE, STUDY_BIAS_SCORE)
        # return str(uploaded_network)
        is_graphml = False
        in_built_network = request.form.get("network_selection")
        ppi_network_contents_df = pd.DataFrame()
        provided_network, ppi_network_contents_df, is_graphml = _get_network_contents(is_graphml, in_built_network,
                                                                                      ppi_network_contents_df,
                                                                                      uploaded_network, NETWORK)
        custom_studybiasdata_input_df = pd.DataFrame()
        study_bias_score_data, custom_studybiasdata_input_df = _get_study_bias_data_contents(
            custom_studybiasdata_input_df, study_bias_score)
        error_statement = _empty_seeds_error(seeds)
        if not error_statement == 'None':
            return render_template('run_robust.html', error=error_statement)
        # return(str(ppi_network_contents_df))
        ppi_network_contents_df, error_statement = _network_error(in_built_network, is_graphml, ppi_network_contents_df)
        if not error_statement == 'None':
            return render_template('run_robust.html', error=error_statement)
        custom_studybiasdata_input_df, error_statement = _custom_study_bias_data_error(study_bias_score,
                                                                                       custom_studybiasdata_input_df)
        if not error_statement == 'None':
            return render_template('run_robust.html', error=error_statement)
        input_dict = _make_input_dict(path_to_graph, seeds, namespace, alpha, beta, n, tau, study_bias_score,
                                      study_bias_score_data, gamma, in_built_network, provided_network, is_graphml)
        celery_running_task.delay(custom_id, input_dict)
        record_taskAdded = Task_Added(custom_id)
        db.session.add(record_taskAdded)
        db.session.commit()
        return render_template('running_celery_task.html', custom_id=custom_id)
    else:
        return render_template('results_get_error.html')


@app.route('/saved_results/<int:saved_id>', methods=['POST', 'GET'])
def retrieve(saved_id):
    found_added_task = _is_added_task(saved_id)
    if found_added_task == 1:
        found_done_task = 0
        done_tasks = Robust.query.all()
        for done_task in done_tasks:
            if str(done_task.custom_id) == str(saved_id):
                retrievedRecord = Robust.query.get(done_task.id)
                found_done_task = 1
        if found_done_task == 1:
            custom_id, path_to_graph, seeds, namespace, alpha, beta, n, tau, study_bias_score, study_bias_score_data, gamma, in_built_network, provided_network, is_graphml, nodeData_str, edgeDataSrc_str, edgeDataDest_str, is_seed_str = query_Robust_database(
                retrievedRecord)
            input_network = _check_input_network(provided_network)
            if nodeData_str == "":
                return render_template('empty_output_returned.html', retrievedRecord=retrievedRecord,
                                       input_network=input_network)
            input_dict = _make_input_dict(path_to_graph, seeds, namespace, alpha, beta, n, tau, study_bias_score,
                                          study_bias_score_data, gamma, in_built_network, provided_network, is_graphml)
            _nodes = _convert_comma_separated_str_to_list(nodeData_str)
            src = _convert_comma_separated_str_to_list(edgeDataSrc_str)
            dest = _convert_comma_separated_str_to_list(edgeDataDest_str)
            _edges = zip(src, dest)
            _is_seed = _convert_comma_separated_str_to_list(is_seed_str)
            is_seed_int = _convert_strList_to_intList(_is_seed)
            node_data = _make_node_data(_nodes, is_seed_int)
            edge_data = _make_edge_data(_edges)
            outputData_dict = _make_dict(node_data, edge_data)
            OutputData_json = _convert_dict_to_json(outputData_dict)
            accessLink = _make_access_link(custom_id)
            input_seeds = _split_data_to_list(seeds)
            title_ = "Saved results - ROBUST"
            return render_template('saved_results.html', retrievedRecord=retrievedRecord, input_dict=input_dict,
                                   OutputData_json=OutputData_json, namespace=namespace, accessLink=accessLink,
                                   input_network=input_network, input_seeds=input_seeds, n=n)
        else:
            return render_template('running_celery_task.html', custom_id=saved_id)
    else:
        return render_template('no_such_task_exists.html', custom_id=saved_id)


def _initialize_input_params(NETWORK, NAMESPACE, STUDY_BIAS_SCORE):
    try:
        namespace = NAMESPACE[int(request.form.get("namespace"))]  # dropdown list
    except:
        namespace = 'GENE_SYMBOL'
    try:
        alpha = float(request.form.get('alpha'))  # number field
    except:
        alpha = 0.25
    try:
        beta = float(request.form.get('beta'))  # number field
    except:
        beta = 0.9
    try:
        n = int(request.form.get('n'))  # number field
    except:
        n = 30
    try:
        tau = float(request.form.get('tau'))  # number field
    except:
        tau = 0.1
    try:
        study_bias_score = STUDY_BIAS_SCORE[int(request.form.get("study_bias_score"))]  # dropdown list
    except:
        study_bias_score = 'No'
    try:
        gamma = float(request.form.get('gamma'))  # number field
    except:
        gamma = 1.0
    try:
        path_to_graph = NETWORK[int(request.form.get('inbuilt_network_selection'))]  # number field
    except:
        path_to_graph = 'BioGRID'
    try:
        uploaded_network = str(request.form.get("uploaded_ppi_network_filename"))
    except:
        pass
    seeds = ''
    try:
        seeds = request.form.get("textbox_seeds")
    except:
        pass
    return namespace, alpha, beta, n, tau, study_bias_score, gamma, path_to_graph, uploaded_network, seeds


def _convert_list_to_comma_separated_string(_list):
    _str = ','.join(_list)
    return _str


def query_Robust_database(retrievedRecord):
    custom_id = retrievedRecord.custom_id
    path_to_graph = retrievedRecord.path_to_graph
    seeds = retrievedRecord.seeds
    namespace = retrievedRecord.namespace
    alpha = retrievedRecord.alpha
    beta = retrievedRecord.beta
    n = retrievedRecord.n
    tau = retrievedRecord.tau
    study_bias_score = retrievedRecord.study_bias_score
    study_bias_score_data = retrievedRecord.study_bias_score_data
    gamma = retrievedRecord.gamma
    in_built_network = retrievedRecord.in_built_network
    provided_network = retrievedRecord.provided_network
    is_graphml = retrievedRecord.is_graphml
    nodeData_str = retrievedRecord.nodeData_str
    edgeDataSrc_str = retrievedRecord.edgeDataSrc_str
    edgeDataDest_str = retrievedRecord.edgeDataDest_str
    is_seed_str = retrievedRecord.is_seed_str
    return custom_id, path_to_graph, seeds, namespace, alpha, beta, n, tau, study_bias_score, study_bias_score_data, gamma, in_built_network, provided_network, is_graphml, nodeData_str, edgeDataSrc_str, edgeDataDest_str, is_seed_str


def _is_added_task(saved_id):
    found_added_task = 0
    added_tasks = Task_Added.query.all()
    for added_task in added_tasks:
        if str(added_task.custom_id) == str(saved_id):
            # retrievedRecord_addedTask = Task_Added.query.get(added_task.id)
            found_added_task = 1
    return found_added_task


def _get_network_contents(is_graphml, in_built_network, ppi_network_contents_df, uploaded_network, NETWORK):
    if in_built_network == "Yes":
        try:
            provided_network = NETWORK[int(request.form.get("inbuilt_network_selection"))]
        except:
            provided_network = 'BioGRID'
    elif in_built_network == "No":
        if not uploaded_network.endswith('.graphml'):
            try:
                provided_network = request.form.get("network_contents")
                data2 = list(map(lambda x: x.split(' '), provided_network.split("\r\n")))
                ppi_network_contents_df = pd.DataFrame(data2[1:], columns=data2[0])
            except:
                pass
        elif uploaded_network.endswith('.graphml'):
            is_graphml = True
            try:
                provided_network = request.form.get("network_contents")
                data2 = list(map(lambda x: x.split(' '), provided_network.split("\r\n")))
                ppi_network_contents_df = pd.DataFrame(data2[1:], columns=data2[0])
            except:
                pass
    return provided_network, ppi_network_contents_df, is_graphml


def _make_input_dict(path_to_graph, seeds, namespace, alpha, beta, n, tau, study_bias_score, study_bias_score_data,
                     gamma, in_built_network, provided_network, is_graphml):
    input_dict = {
        "path_to_graph": path_to_graph,
        "seeds": seeds,
        "namespace": namespace,
        "alpha": alpha,
        "beta": beta,
        "n": n,
        "tau": tau,
        "study_bias_score": study_bias_score,
        "study_bias_score_data": study_bias_score_data,
        "gamma": gamma,
        "in_built_network": in_built_network,
        "provided_network": provided_network,
        "is_graphml": is_graphml
    }
    return input_dict


def _custom_study_bias_data_error(study_bias_score, custom_studybiasdata_input_df):
    if study_bias_score == 'CUSTOM':
        if custom_studybiasdata_input_df.empty:
            error_statement = 'Custom study bias data has to be uploaded!'
        else:
            numRows_df = custom_studybiasdata_input_df.shape[0]
            if numRows_df == 0:
                error_statement = 'Custom study bias data with zero rows uploaded. Please add atleast one row excluding the column headers.'
            else:
                if custom_studybiasdata_input_df.shape[1] < 2:
                    error_statement = 'Custom study bias data with less than two columns uploaded. Please add two columns.'
                elif custom_studybiasdata_input_df.shape[1] >= 2:
                    custom_studybiasdata_input_df = custom_studybiasdata_input_df.iloc[:, :2]
                    error_statement = 'None'
    else:
        error_statement = 'None'
    return custom_studybiasdata_input_df, error_statement


def _network_error(in_built_network, is_graphml, ppi_network_contents_df):
    if in_built_network == "No":
        if not is_graphml == True:
            if ppi_network_contents_df.empty:
                error_statement = 'Custom network has to be uploaded!'
            else:
                numRows_df2 = ppi_network_contents_df.shape[0]
                if numRows_df2 == 0:
                    error_statement = 'Custom network with zero rows uploaded. Please add atleast one row excluding the column headers.'
                else:
                    if ppi_network_contents_df.shape[1] < 2:
                        error_statement = 'Custom network with less than two columns uploaded. Please add two columns.'
                    elif ppi_network_contents_df.shape[1] >= 2:
                        # Custom network with more than two columns uploaded. First two columns retained:
                        ppi_network_contents_df = ppi_network_contents_df.iloc[:, :2]
                        error_statement = 'None'
        else:
            error_statement = 'None'
    else:
        error_statement = 'None'
    return ppi_network_contents_df, error_statement


def _empty_seeds_error(seeds):
    if seeds == '' or seeds == None:
        error_statement = 'Seeds cannot be empty'
    else:
        error_statement = 'None'
    return error_statement


def _get_study_bias_data_contents(custom_studybiasdata_input_df, study_bias_score):
    if study_bias_score == 'CUSTOM':
        try:
            study_bias_score_data = request.form.get("custom_studybiasdata_contents_textbox")
            data = list(map(lambda x: x.split(' '), study_bias_score_data.split("\r\n")))
            custom_studybiasdata_input_df = pd.DataFrame(data[1:], columns=data[0])
        except:
            pass
    else:
        study_bias_score_data = study_bias_score
    return study_bias_score_data, custom_studybiasdata_input_df


def _initialize_dropdown_params():
    network = ['BioGRID', 'APID', 'STRING']
    namespace = ['GENE_SYMBOL', 'UNIPROT', 'ENTREZ']
    study_bias_score = ['No', 'BAIT_USAGE', 'STUDY_ATTENTION', 'CUSTOM']
    return network, namespace, study_bias_score


def _generate_custom_id():
    s = shortuuid.ShortUUID(alphabet="0123456789")
    custom_id = s.random(length=5)
    return custom_id


def _convert_strList_to_intList(str_list):
    intList = []
    for i in str_list:
        intList.append(int(i))
    return intList


def _convert_comma_separated_str_to_list(str_data):
    list_data = str_data.split(",")
    return list_data


def _make_node_data(_nodes, is_seed_int):
    node_data = []
    for i in range(len(_nodes)):
        if is_seed_int[i] == 1:
            node_dict = {"id": _nodes[i], "group": "important"}
        else:
            node_dict = {"id": _nodes[i], "group": "gene"}
        node_data.append(node_dict)
    return node_data


def _make_edge_data(_edges):
    edge_data = []
    for i, j in _edges:
        edge_dict = {"from": i, "to": j, "group": "default"}
        edge_data.append(edge_dict)
    return edge_data


def _make_dict(node_data, edge_data):
    outputData_dict = {"nodes": node_data, "edges": edge_data}
    return outputData_dict


def _convert_dict_to_json(outputData_dict):
    OutputData_json = json.dumps(outputData_dict)
    return OutputData_json


def _make_access_link(id):
    import os
    host_url = os.environ.get('HOST', '127.0.0.1:5000')
    accessLink = f'{host_url}/saved_results/' + str(id)
    return accessLink


def _check_input_network(provided_network):
    if provided_network in ['BioGRID', 'APID', 'STRING']:
        input_network = provided_network
    else:
        input_network = 'custom'
    return input_network


def _split_data_to_list(data):
    str_data = str(data)
    list_data = str_data.split()
    return list_data


if __name__ == '__main__':
    scheduler.add_job(id='Updation of study bias scores', func=update_study_bias_scores_scheduled_task,
                      trigger="interval", seconds=30000)
    scheduler.add_job(id='Updation of networks', func=update_networks_scheduled_task, trigger="interval", seconds=30000)
    scheduler.start()
    db.create_all()
    app.run(debug=False, host='0.0.0.0')
