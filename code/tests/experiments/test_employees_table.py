import pytest
from boto3.dynamodb.conditions import Key


def create_employee(*, table):
    user = {
        "emp_id": 1,
        "first_name": "Jon",
        "last_name": "Doe",
        "email": "jdoe@test.com",
    }
    table.put_item(Item=user)


def query_data_with_gsi(*, table):
    return table.query(
        IndexName="email",
        KeyConditionExpression=Key("email").eq("jdoe@test.com"),
    )["Items"]


@pytest.mark.skip
def test_query_data_with_gsi(employees_table):
    create_employee(table=employees_table)
    resp = query_data_with_gsi(table=employees_table)
    print(resp)  # noqa: T001
