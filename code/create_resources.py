import argparse
import base64
import json
import os
from typing import Any, Dict

import boto3
from table_list import TABLE_LIST

SSM_AUTH_KEY_PARAM_NAME = "/vonavi-shop-app/auth-key"


def create_table(*, table: Dict[str, Any]) -> str:
    table_name = table["TableName"]
    client = boto3.client("dynamodb")
    client.create_table(**table)
    waiter = client.get_waiter("table_exists")
    waiter.wait(TableName=table_name, WaiterConfig={"Delay": 1})
    return table_name


def record_as_env_var(key, value, stage):
    with open(os.path.join(".chalice", "config.json")) as f:
        data = json.load(f)
        data["stages"].setdefault(stage, {}).setdefault(
            "environment_variables", {}
        )[key] = value
    with open(os.path.join(".chalice", "config.json"), "w") as f:
        serialized = json.dumps(data, indent=2, separators=(",", ": "))
        f.write(serialized + "\n")


def _already_in_config(env_var, stage):
    with open(os.path.join(".chalice", "config.json")) as f:
        return env_var in json.load(f)["stages"].get(stage, {}).get(
            "environment_variables", {}
        )


def create_auth_key_if_needed(stage):
    ssm = boto3.client("ssm")

    try:
        ssm.get_parameter(Name=SSM_AUTH_KEY_PARAM_NAME)
    except ssm.exceptions.ParameterNotFound:
        print(f"Generating auth key.")
        kms = boto3.client("kms")
        random_bytes = kms.generate_random(NumberOfBytes=32)["Plaintext"]
        encoded_random_bytes = base64.b64encode(random_bytes).decode()
        ssm.put_parameter(
            Name=SSM_AUTH_KEY_PARAM_NAME,
            Value=encoded_random_bytes,
            Type="SecureString",
        )


def create_resources(args):
    for table in TABLE_LIST:
        env_var = table["env_var"]

        if _already_in_config(env_var, args.stage):
            continue

        print(f"Creating table: {table['TableName']}")
        del table["env_var"]
        table_name = create_table(table=table)
        record_as_env_var(env_var, table_name, args.stage)

    create_auth_key_if_needed(args.stage)


def cleanup_resources(args):
    ddb = boto3.client("dynamodb")
    ssm = boto3.client("ssm")
    with open(os.path.join(".chalice", "config.json")) as f:
        config = json.load(f)
        env_vars = (
            config["stages"]
            .get(args.stage, {})
            .get("environment_variables", {})
        )
        for key in list(env_vars):
            value = env_vars.pop(key)
            if key.endswith("_TABLE_NAME"):
                print(f"Deleting table: {value}")
                ddb.delete_table(TableName=value)
        if not env_vars:
            del config["stages"][args.stage]["environment_variables"]
    try:
        print(f"Deleting SSM param: {SSM_AUTH_KEY_PARAM_NAME}")
        ssm.delete_parameter(Name=SSM_AUTH_KEY_PARAM_NAME)
    except Exception:
        pass

    with open(os.path.join(".chalice", "config.json"), "w") as f:
        serialized = json.dumps(config, indent=2, separators=(",", ": "))
        f.write(serialized + "\n")

    print(
        "Resources deleted.  If you haven't already, be "
        "sure to run 'chalice delete' to delete your Chalice application."
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--stage", default="dev")
    parser.add_argument("-c", "--cleanup", action="store_true")
    args = parser.parse_args()
    if args.cleanup:
        cleanup_resources(args)
    else:
        create_resources(args)


if __name__ == "__main__":
    main()
