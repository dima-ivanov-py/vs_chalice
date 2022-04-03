import json
import os
from typing import Any, Dict

import boto3
from chalicelib.services.products.create_product import CreateProductService
from chalicelib.services.products.delete_product import DeleteProductService


def get_client():
    return boto3.client("dynamodb")


def get_resource():
    return boto3.resource("dynamodb")


def get_client_local():
    return boto3.client("dynamodb", endpoint_url="http://localhost:8000")


def get_resource_local():
    return boto3.resource("dynamodb", endpoint_url="http://localhost:8000")


def get_resources(local=True):
    resources = {"client": get_client, "resource": get_resource}
    if local:
        resources["client"] = get_client_local
        resources["resource"] = get_resource_local
    return resources


RESOURCES = get_resources()


def create_table(*, table, table_name):
    client = RESOURCES["client"]()
    resource = RESOURCES["resource"]()
    del table["env_var"]
    table["TableName"] = table_name
    resource.create_table(**table)
    waiter = client.get_waiter("table_exists")
    waiter.wait(TableName=table_name, WaiterConfig={"Delay": 1})
    return resource.Table(table_name)


def delete_table(*, table_name):
    client = RESOURCES["client"]()
    client.delete_table(TableName=table_name)
    waiter = client.get_waiter("table_not_exists")
    waiter.wait(TableName=table_name, WaiterConfig={"Delay": 1})


def clear_products_table(*, table):
    delete_service = DeleteProductService(table=table)
    for item in table.scan()["Items"]:
        delete_service.set_uid(uid=item["uid"])
        delete_service.set_username(username=item["username"])
        delete_service()


def clear_users_table(*, table):
    items = table.scan()["Items"]
    for item in items:
        table.delete_item(Key={"username": item["username"]})


def create_products(*, products_dict, table):
    create_service = CreateProductService(table=table)
    for product in products_dict.keys():
        create_service.set_data(data=products_dict[product])
        create_service()


def create_users(*, users_dict, table):
    for user in users_dict.items():
        table.put_item(Item=user[1])


PATH_TO_CONFIG = (
    "/home/metanoia/Documents/projects/vs_chalice/code/.chalice/config.json"
)


def get_data_from_json_file(filename: str = PATH_TO_CONFIG) -> Dict[str, Any]:
    with open(filename) as json_file:
        return json.load(json_file)


def set_env():
    data = get_data_from_json_file()
    variables = data["stages"]["dev"]["environment_variables"]
    os.environ = {**os.environ, **variables}  # noqa: B003
