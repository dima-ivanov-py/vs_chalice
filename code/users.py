import argparse
import base64
import getpass
import hashlib
import hmac
import json
import os

import boto3
from boto3.dynamodb.types import Binary
from chalicelib.selectors.get_user import get_user_selector


def get_table_name(stage):
    with open(os.path.join(".chalice", "config.json")) as f:
        data = json.load(f)
    return data["stages"][stage]["environment_variables"]["USERS_TABLE_NAME"]


def create_user(stage):
    table_name = get_table_name(stage)
    table = boto3.resource("dynamodb").Table(table_name)
    username = input("Username: ")
    statuses = {"seller": "SELLER", "customer": "CUSTOMER"}

    try:
        exists = get_user_selector(table, username)
        if exists:
            raise ValueError(f"User with name '{username}' already exists!")
    except KeyError:
        pass

    while True:
        try:
            status = input("Status: ")
            status = statuses[status]
            break
        except KeyError:
            pass

    username.strip()
    password = getpass.getpass("Password: ").strip()
    password_fields = encode_password(password)
    item = {
        "username": username,
        "status": status,
        "hash": password_fields["hash"],
        "salt": Binary(password_fields["salt"]),
        "rounds": password_fields["rounds"],
        "hashed": Binary(password_fields["hashed"]),
    }
    table.put_item(Item=item)


def encode_password(password, salt=None):
    if salt is None:
        salt = os.urandom(32)
    rounds = 100000
    hashed = hashlib.pbkdf2_hmac(
        "sha256", password.encode("utf-8"), salt, rounds
    )
    return {"hash": "sha256", "salt": salt, "rounds": rounds, "hashed": hashed}


def list_users(stage):
    table_name = get_table_name(stage)
    table = boto3.resource("dynamodb").Table(table_name)
    for item in table.scan()["Items"]:
        print(item["username"])


def get_user(username, stage):
    table_name = get_table_name(stage)
    table = boto3.resource("dynamodb").Table(table_name)
    user_record = table.get_item(Key={"username": username}).get("Item")
    if user_record is not None:
        print(f"Entry for user: {username}")
        for key, value in user_record.items():
            if isinstance(value, Binary):
                value = base64.b64encode(value.value).decode()
            print(f"  {key:10}: {value}")


def test_password(stage):
    username = input("Username: ").strip()
    password = getpass.getpass("Password: ").strip()
    table_name = get_table_name(stage)
    table = boto3.resource("dynamodb").Table(table_name)
    item = table.get_item(Key={"username": username})["Item"]
    encoded = encode_password(password, salt=item["salt"].value)

    if hmac.compare_digest(encoded["hashed"], item["hashed"].value):
        print("Password verified.")
    else:
        print("Password verification failed.")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--create-user", action="store_true")
    parser.add_argument("-t", "--test-password", action="store_true")
    parser.add_argument("-g", "--get-user")
    parser.add_argument("-s", "--stage", default="dev")
    parser.add_argument("-l", "--list-users", action="store_true")
    args = parser.parse_args()

    if args.create_user:
        create_user(args.stage)
    elif args.list_users:
        list_users(args.stage)
    elif args.test_password:
        test_password(args.stage)
    elif args.get_user is not None:
        get_user(args.get_user, args.stage)


if __name__ == "__main__":
    main()
