import pytest
from boto3.dynamodb.conditions import Key

USER = {
    "email": "jdoe@test.com",
    "username": "username",
    "last_name": "Doe",
    "first_name": "Eric",
}


def get_item(*, table, username):
    return table.get_item(Key={"username": username})


def query(*, table, username):
    return table.query(KeyConditionExpression=Key("username").eq(username))


def update(*, table, username):
    return table.update_item(
        Key={"username": username},
        UpdateExpression="set first_name = :g",
        ExpressionAttributeValues={":g": "Jane"},
        ReturnValues="UPDATED_NEW",
    )


def delete(*, table, username):
    return table.delete_item(Key={"username": username})


def create_bunch_of_users(*, table):
    for n in range(3):
        table.put_item(
            Item={
                "username": f"user_{n}",
                "first_name": "Jon",
                "last_name": f"Doe{n}",
                "email": f"jdoe{n}@test.com",
            }
        )


def scan_first_and_last_names(*, table):
    return table.scan(ProjectionExpression="first_name, last_name")


def multi_part_scan(*, table):
    response = table.scan(Limit=1)
    result = response["Items"]

    while "LastEvaluatedKey" in response:
        response = table.scan(ExclusiveStartKey=response["LastEvaluatedKey"])
        result.extend(response["Items"])

    return result


@pytest.mark.skip
def test_get_item(users_table):
    users_table.put_item(Item=USER)
    resp = get_item(table=users_table, username=USER["username"])
    if "Item" in resp:
        print(resp["Item"])  # noqa


@pytest.mark.skip
def test_query(users_table):
    users_table.put_item(Item=USER)
    resp = query(table=users_table, username=USER["username"])
    if "Items" in resp:
        print(resp["Items"])  # noqa


@pytest.mark.skip
def test_update(users_table):
    users_table.put_item(Item=USER)
    update(table=users_table, username=USER["username"])
    resp = get_item(table=users_table, username=USER["username"])
    if "Item" in resp:
        print(resp["Item"])  # noqa


@pytest.mark.skip
def test_delete(users_table):
    users_table.put_item(Item=USER)
    delete(table=users_table, username=USER["username"])
    resp = get_item(table=users_table, username=USER["username"])
    if "Item" in resp:
        print(resp["Item"])  # noqa


@pytest.mark.skip
def test_scan(users_table):
    create_bunch_of_users(table=users_table)
    resp = scan_first_and_last_names(table=users_table)
    if "Items" in resp:
        print(resp["Items"])  # noqa


@pytest.mark.skip
def test_multi_part_scan(users_table):
    create_bunch_of_users(table=users_table)
    resp = multi_part_scan(table=users_table)
    print(resp)  # noqa
