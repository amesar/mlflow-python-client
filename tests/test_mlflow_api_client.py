

import time
import pytest
import unittest
from mlflow_client.mlflow_api_client import MLflowApiClient

api_url="http://localhost:5001"
client = MLflowApiClient(api_url)

def create_exp_name():
    return "exp_"+str(time.time()).replace(".","")

class ApiTest(unittest.TestCase):
    def setUp(self):
        pass

    def test_create_experiment(self):
        experiment_name = create_exp_name()
        rsp = client.create_experiment(experiment_name)
        experiment_id = rsp['experiment_id']

        rsp = client.get_experiment(experiment_id)
        print("Experiment:",rsp)
        exp = rsp['experiment']
        assert exp['experiment_id'] == experiment_id
        assert exp['name'] == experiment_name


