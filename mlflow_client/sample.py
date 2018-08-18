from __future__ import print_function

import os, sys, time
from mlflow_api_client import MLflowApiClient

def now():
    return long(time.time())

def process(client):
    print("====== list_experiments")
    exps = client.list_experiments()
    print("list_experiments: #experiments:",len(exps))
    for exp in exps:
        print(" ",exp)
   
    print("====== create_experiment")
    experiment_name = "py_exp_"+str(time.time()).replace(".","")
    print("CreateExperiment: req: experiment_name:",experiment_name)
    experiment_id = client.create_experiment(experiment_name)
    print("create_experiment: rsp.experiment_id:",experiment_id)

    print("====== create_run")
    run_name = 'run_for_exp_' + experiment_name
    current_file = os.path.basename(__file__)
    start_time = now()
    dct = {'experiment_id': experiment_id, 'run_name': run_name, 'source_type': 'LOCAL', 'source_name': current_file, 'start_time': start_time }
    rsp = client.create_run(dct)
    print("create_run rsp:",rsp)
    run_uuid = rsp['run_uuid']

    print("====== Log params and metrics")
    param_key = 'max_depth'
    metric_key = 'auc'
    client.log_parameter(run_uuid, param_key, '2')
    client.log_metric(run_uuid, metric_key, .99)

    print("====== update_run Run")
    dct = {'run_uuid': run_uuid, 'status': 'FINISHED', 'end_time': start_time+1000 }
    print("update_run req:",dct)
    client.update_run(dct)

    print("====== get_run")
    run = client.get_run(run_uuid)
    print("get_run rsp:",run)

    print("====== get_experiment")
    exp = client.get_experiment(experiment_id)
    print("get_experiment rsp:",exp)

    print("====== get_metric")
    rsp = client.get_metric(run_uuid, metric_key)
    print("get_metric rsp:",rsp)

    print("====== get_metric_history")
    rsp = client.get_metric_history(run_uuid, metric_key)
    print("get_metric_history rsp:",rsp)

    print("====== list_artifacts")
    path = ''
    rsp = client.list_artifacts(run_uuid, path)
    print("list_artifacts rsp:",rsp)

    print("====== Search")
    expIds = [ experiment_id]
    clauses = [
        { 'type': 'parameter', 'comparator': '=', 'key': param_key, 'value': '2'},
        { 'type': 'metric', 'comparator': '>=', 'key': metric_key, 'value': .99} ]
    rsp = client.search2(expIds,clauses)
    print("search2 rsp:",rsp)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.stderr.write("ERROR: Expecting BASE_URL")
        sys.exit(1)
    client = MLflowApiClient(sys.argv[1])
    process(client)
