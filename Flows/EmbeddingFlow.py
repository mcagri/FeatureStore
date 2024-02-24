from prefect import flow, task, serve
from prefect_dask.task_runners import DaskTaskRunner
from pymongo import MongoClient
import configparser
import pandas as pd
import requests
import json

config = configparser.ConfigParser()
config.read("../Config/db.config")
username = config['MONGODB']['MONGO_USER']
pwd = config['MONGODB']['MONGO_PASSWORD']
dbname = config['MONGODB']['MONGO_DB']
url = config['MONGODB']['MONGO_URL']
port = config['MONGODB']['MONGO_PORT']
client = MongoClient(url,
                         username=username,
                         password=pwd,
                         authSource="admin",
                         authMechanism='SCRAM-SHA-256')
db = client[dbname]
collection = db['Product']

@task
def process_document(path: str):
    products = pd.read_csv(path).to_dict('records')
    return products

@task
def embedding(id: int, product: dict):
    url = "http://127.0.0.1:15001/embedtext"
    headers = {
        'Content-Type': 'application/json'
    }


    payload = json.dumps({
        "id": id,
        "text": product['title']
    })
    response = requests.request("POST", url, headers=headers, data=payload)
    product['embedding'] = response.json()['embedding']

    collection.insert_one(product)


@flow(task_runner=DaskTaskRunner())
def parallel_runner(products):
    for i, product in enumerate(products):
        embedding(i, product)


@flow(log_prints=True)
def feature_store_update():
    path = "../Data/home_depot_data_1_2021_12.csv"
    products = process_document(path)
    parallel_runner(products)


if __name__ == "__main__":
    feature_store_update.serve(name="feature_store_deployment",
    interval = 60,
    tags = ["medium", "featurestore"],
    description = "Process an example dataset, create embeddings for product names and store them in mongodb collection",
    )