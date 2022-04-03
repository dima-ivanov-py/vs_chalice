import pytest
from boto3.dynamodb.conditions import Key


def create_books(*, table):
    book = {
        "title": "This is a Good Book",
        "author": "Jon Doe",
        "year": "1980",
    }

    another_book = {
        "title": "This is a Good Book",
        "author": "Jane Doe",
        "year": "1998",
    }

    table.put_item(Item=book)
    table.put_item(Item=another_book)


def fetch_data_with_range_1(*, table):
    return table.get_item(
        Key={"title": "This is a Good Book", "author": "Jane Doe"}
    )["Item"]


def fetch_data_with_range_2(*, table):
    return table.query(
        KeyConditionExpression=Key("title").eq("This is a Good Book")
        & Key("author").eq("Jon Doe")
    )["Items"]


@pytest.mark.skip
def test_fetch_data_with_range(books_table):
    create_books(table=books_table)
    resp = fetch_data_with_range_1(table=books_table)
    print(resp)  # noqa: T001
