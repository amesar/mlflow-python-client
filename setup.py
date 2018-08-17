from setuptools import setup, find_packages

setup(name='mlflow-python-client',
      version='0.0.1',
      description='Low-level Python client for MLflow API',
      author='andre',
      packages = find_packages(),
      zip_safe=False,
      install_requires=[
          'requests'
      ]
)
