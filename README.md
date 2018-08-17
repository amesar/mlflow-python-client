# MLflow Python Client

Python client for [MLflow](https://mlflow.org) REST API.

See [api_client.py](mlflow_client/api_client.py).

## Build
```
pip install requests
```

## Run
Have a [MLflow Tracking Server 0.4.2](https://mlflow.org/docs/latest/tracking.html#running-a-tracking-server) running.

Run [sample.py](mlflow_client/sample.py).

```
cd mlflow_client
python sample.py http://localhost:5000
```
