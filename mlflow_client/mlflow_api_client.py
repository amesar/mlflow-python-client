from __future__ import print_function

import requests
import json
import time

class MLflowApiClient(object):
    """ HTTP Client for MLflow API """

    def __init__(self, api_uri, verbose=True):
        self.base_uri = api_uri + "/api/2.0/preview/mlflow"
        self.verbose = verbose
        if self.verbose: print("api_client: base_uri:",self.base_uri)

    def list_experiments(self):
        return self.get('experiments/list')['experiments']

    def get_experiment(self, experiment_id):
        """
        :param experiment_id: experiment ID search over
        """
        return self.get('experiments/get?experiment_id='+experiment_id)

    def create_experiment(self, experiment_name):
        """
        :param experiment_name: experiment name
        :returns: experiment ID 
        :rtype: str
        """
        dct = {'name': experiment_name}
        return self.post('experiments/create',dct)['experiment_id']

    def get_run(self, run_uuid):
        return self.get('runs/get?run_uuid='+run_uuid)

    def create_run(self, dct):
        return self.post('runs/create',dct)['run']['info']

    def update_run(self, dct):
        return self.post('runs/update',dct)

    def log_parameter(self, run_uuid, key, value):
        dct = {'run_uuid': run_uuid, 'key': key, 'value': value}
        return self.post('runs/log-parameter',dct)

    def log_metric(self, run_uuid, key, value):
        dct = {'run_uuid': run_uuid, 'key': key, 'value': value, 'timestamp': self._now()}
        return self.post('runs/log-metric',dct)

    def get_metric(self, run_uuid, metric_key):
        return self.get('metrics/get?run_uuid={}&metric_key={}'.format(run_uuid,metric_key))

    def get_metric_history(self, run_uuid, metric_key):
        return self.get('metrics/get-history?run_uuid={}&metric_key={}'.format(run_uuid,metric_key))

    def list_artifacts(self, run_uuid, path):
        return self.get('artifacts/list?run_uuid={}&path={}'.format(run_uuid,path))

    def get_artifact(self, run_uuid, path):
        return self.get_as_bytes('artifacts/get?run_uuid={}&path={}'.format(run_uuid,path))

    def search(self, dct):
        return self.post('runs/search',dct)

    def search2(self, experiment_ids, clauses):
        """
        :param experiment_ids: List of experiment IDs to search over
        :param clauses: List of simplified clauses 
            Example: [
                { "type": "parameter", "comparator": "=", "key": "max_depth", "value": "3" },
                { "type": "metric", "comparator": ">=", "key": "auc", "value": 2 } 
             ] 
        """
        anded_expressions = []
        for cl in clauses: 
            ctype = cl['type']
            if ctype == 'parameter':
                anded_expressions.append({'parameter': { 'key': cl['key'], 'string': { 'comparator': cl['comparator'], 'value': cl['value'] }}})
            elif ctype == 'metric':
                anded_expressions.append({'metric': { 'key': cl['key'], 'float': { 'comparator': cl['comparator'], 'value': cl['value'] }}})
            else:
                raise Exception("Illegal clause type '{}' in search".format(ctype))
        return self.search({ 'experiment_ids':  experiment_ids, 'anded_expressions': anded_expressions })


    def get_experiment_id(self, experiment_name):
        exps = self.list_experiments()
        for exp in exps:
            if experiment_name == exp['name']:
                return exp['experiment_id']
        return None

    def get_or_create_experiment_id(self, experiment_name):
        experiment_id = self.get_experiment_id(experiment_name)
        if experiment_id is None:
            experiment_id = self.create_experiment(experiment_name)
        #print("experiment_name={} experiment_id={}".format(experiment_name,experiment_id))
        return experiment_id


    def _mk_url(self, path):
        return self.base_uri + '/' + path

    def get(self, path):
        rsp = self._get(path)
        if self.verbose: print("api_client.GET: rsp:",rsp)
        return json.loads(str(rsp))

    def _get(self, path):
        """ Executes an HTTP GET call
        :param path: Relative path name such as runs/get.
        """
        url = self._mk_url(path)
        if self.verbose: print("api_client.GET: url:",url)
        rsp = requests.get(url)
        self._check_response(rsp)
        return rsp.text

    def get_as_bytes(self, path):
        url = self._mk_url(path)
        if self.verbose: print("api_client.GET: url:",url)
        rsp = requests.get(url)
        self._check_response(rsp)
        return rsp.content

    def post(self, path, dct):
        data = json.dumps(dct)
        if self.verbose: print("api_client.POST: req:",data)
        rsp = self._post(path, data)
        if self.verbose: print("api_client.POST: rsp:",rsp)
        return json.loads(str(rsp))

    def _post(self, path, data):
        """
        Executes an HTTP POST call
        :param path: Relative path name such as runs/get.
        :param data: JSON request payload.
        """
        url = self._mk_url(path)
        if self.verbose: print("api_client.POST: url:",url)
        rsp = requests.post(url, data)
        self._check_response(rsp)
        return rsp.text

    def _check_response(self, rsp):
        if rsp.status_code < 200 or rsp.status_code > 299:
            raise Exception("HTTP status code: " + str(rsp.status_code)+" Reason: "+rsp.reason)

    def _now(self):
        return int(time.time())
