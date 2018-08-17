# MLflow Python Client

Python client for [MLflow](https://mlflow.org) REST API.

See [api_client.py](mlflow_client/api_client.py).

## Build
Basic
```
pip install requests
```

Of if you want to build an egg in dist/mlflow_python_client-0.0.1-py2.7.egg
```
python setup.py bdist_egg
```

## Run
Make sure you have an [MLflow Tracking Server 0.4.2](https://mlflow.org/docs/latest/tracking.html#running-a-tracking-server) running.

Run [sample.py](mlflow_client/sample.py).

```
cd mlflow_client
python sample.py http://localhost:5000
```

Output from [samples/out.log](samples/out.log).
```
api_client: base_uri: http://localhost:5011/api/2.0/preview/mlflow
====== get_experiments
api_client.GET: url: http://localhost:5011/api/2.0/preview/mlflow/experiments/list
api_client.GET: rsp: {
  "experiments": [
    {
      "experiment_id": "0",
      "name": "Default",
      "artifact_location": "/home/andre/work/mlflow/test/mlruns/0"
    },

. . .

api_client.POST: req: {"anded_expressions": [{"parameter": {"string": {"value": "2", "comparator": "="}, "key": "max_depth"}}, {"metric": {"float": {"value": 0.99, "comparator": ">="}, "key": "auc"}}], "experiment_ids": ["10"]}

. . .

SearchResult: {u'runs': [{u'info': {u'status': u'FINISHED', u'source_name': u'sample.py', u'name': u'Run 0', u'artifact_uri': u'/home/andre/work/mlflow/test/mlruns/10/1b3aa6904fa042d3854fb77f38fce92f/artifacts', u'start_time': u'1534530257', u'source_type': u'LOCAL', u'run_uuid': u'1b3aa6904fa042d3854fb77f38fce92f', u'end_time': u'1534531257', u'experiment_id': u'10', u'user_id': u''}, u'data': {u'metrics': [{u'timestamp': u'1534530257', u'value': 0.9900000095367432, u'key': u'auc'}], u'params': [{u'value': u'2', u'key': u'max_depth'}]}}]}
```
