from __future__ import print_function

import os, sys, time
from api_client import ApiClient

def now():
    return long(time.time())

def process(client):
    print("====== get_experiments")
    exps = client.get_experiments()
    print("Experiments.type:",type(exps))
    print("#Experiments:",len(exps))
    for exp in exps:
        print(" ",exp)
   
    print("====== CreateExperiment")
    experiment_name = "py_exp_"+str(time.time()).replace(".","")
    print("CreateExperiment: req: experiment_name:",experiment_name)
    rsp = client.create_experiment(experiment_name)
    experiment_id = rsp['experiment_id']
    print("CreateExperiment: rsp: experiment_id:",experiment_id)

    print("====== CreateRun")
    run_name = 'run_for_exp_' + experiment_name
    current_file = os.path.basename(__file__)
    start_time = now()
    dct = {'experiment_id': experiment_id, 'run_name': run_name, 'source_type': 'LOCAL', 'source_name': current_file, 'start_time': start_time }
    rsp = client.create_run(dct)
    print("CreateRun: rsp:",rsp)
    run_uuid = rsp['run_uuid']

    print("====== Log")
    client.log_parameter(run_uuid, 'max_depth', '2')
    client.log_metric(run_uuid, 'auc', .99)

    print("====== Update Run")
    dct = {'run_uuid': run_uuid, 'status': 'FINISHED', 'end_time': start_time+1000 }
    client.update_run(dct)

    print("====== GetRun")
    run = client.get_run(run_uuid)
    print("GetRun:",run)

    print("====== get_experiment")
    exp = client.get_experiment(experiment_id)
    print("Experiment:",exp)

    print("====== Search")
    expIds = [ experiment_id]
    clauses = [
        { 'type': 'parameter', 'comparator': '=', 'key': 'max_depth', 'value': '2'},
        { 'type': 'metric', 'comparator': '>=', 'key': 'auc', 'value': .99} ]
    rsp = client.search2(expIds,clauses)
    print("SearchResult:",rsp)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.stderr.write("ERROR: Expecting BASE_URL")
        sys.exit(1)
    client = ApiClient(sys.argv[1])
    process(client)
