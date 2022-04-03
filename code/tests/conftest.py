from uuid import uuid4

import app
import pytest
import tables
from boto3.dynamodb.types import Binary
from chalice.test import Client
from chalicelib.auth.auth_key_getter import get_auth_key
from chalicelib.auth.jwt_token_getter import get_jwt_token
from tests.utils import (
    clear_products_table,
    clear_users_table,
    create_products,
    create_table,
    create_users,
    delete_table,
    set_env,
)
from users import encode_password

set_env()


@pytest.fixture
def client():
    with Client(app.app) as client:
        yield client


@pytest.fixture(scope="session")
def users_table():
    table_name = str(uuid4())
    yield create_table(table=tables.USERS_TABLE, table_name=table_name)
    delete_table(table_name=table_name)


@pytest.fixture(scope="session")
def products_table():
    table_name = str(uuid4())
    yield create_table(table=tables.PRODUCTS_TABLE, table_name=table_name)
    delete_table(table_name=table_name)


@pytest.fixture(scope="session")
def orders_table():
    table_name = str(uuid4())
    yield create_table(table=tables.ORDERS_TABLE, table_name=table_name)
    delete_table(table_name=table_name)


@pytest.fixture
def products(products_table):
    products_of_user_1 = {
        f"product_{i}": {
            "title": str(uuid4()),
            "price": i + 100,
            "username": "username_1",
            "uid": str(uuid4()),
        }
        for i in range(6)
    }

    products_of_user_2 = {
        f"product_{i}": {
            "title": str(uuid4()),
            "price": i + 200,
            "username": "username_2",
            "uid": str(uuid4()),
        }
        for i in range(3)
    }

    products_of_user_3 = {
        f"product_{i}": {
            "title": str(uuid4()),
            "price": i + 300,
            "username": "username_3",
            "uid": str(uuid4()),
        }
        for i in range(7)
    }

    create_products(products_dict=products_of_user_1, table=products_table)
    create_products(products_dict=products_of_user_2, table=products_table)
    create_products(products_dict=products_of_user_3, table=products_table)

    yield {
        "table": products_table,
        "products_of_user_1": products_of_user_1,
        "products_of_user_2": products_of_user_2,
        "products_of_user_3": products_of_user_3,
    }

    clear_products_table(table=products_table)


@pytest.fixture
def users(users_table):
    users_dict = {}
    for user in range(11):
        password = f"password_{user}"
        password_fields = encode_password(password)
        item = {
            "username": f"username_{user}",
            "status": "CUSTOMER",
            "hash": password_fields["hash"],
            "salt": Binary(password_fields["salt"]),
            "rounds": password_fields["rounds"],
            "hashed": Binary(password_fields["hashed"]),
        }

        users_dict[f"user_{user}"] = item

    create_users(users_dict=users_dict, table=users_table)

    yield {"table": users_table, "users": users_dict}

    clear_users_table(table=users_table)


@pytest.fixture(scope="session")
def books_table():
    table_name = str(uuid4())
    yield create_table(table=tables.BOOKS_TABLE, table_name=table_name)
    delete_table(table_name=table_name)


@pytest.fixture(scope="session")
def employees_table():
    table_name = str(uuid4())
    yield create_table(table=tables.EMPLOYEES_TABLE, table_name=table_name)
    delete_table(table_name=table_name)


@pytest.fixture(scope="session")
def posts_table():
    table_name = str(uuid4())
    yield create_table(table=tables.POSTS_TABLE, table_name=table_name)
    delete_table(table_name=table_name)


@pytest.fixture(scope="session")
def carts_table():
    table_name = str(uuid4())
    yield create_table(table=tables.CARTS_TABLE, table_name=table_name)
    delete_table(table_name=table_name)


@pytest.fixture(scope="session")
def authorized_user_token(users_table):
    password = "authorized_user_password"  # noqa: S105
    password_fields = encode_password(password)
    users_dict = {}
    username = "authorized_username"

    item = {
        "username": username,
        "status": "SELLER",
        "hash": password_fields["hash"],
        "salt": Binary(password_fields["salt"]),
        "rounds": password_fields["rounds"],
        "hashed": Binary(password_fields["hashed"]),
    }

    users_dict["authorized_user"] = item
    create_users(users_dict=users_dict, table=users_table)
    record = users_table.get_item(Key={"username": username}).get("Item")
    auth_key = get_auth_key()

    return {
        "table": users_table,
        "username": username,
        "password": password,
        "token": get_jwt_token(
            username=username,
            password=password,
            auth_key=auth_key,
            record=record,
        ),
    }
