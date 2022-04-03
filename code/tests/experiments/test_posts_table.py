import pytest
from boto3.dynamodb.conditions import Key


def create_posts(*, table):
    post1 = {
        "title": "My favorite hiking spots",
        "user_name": "jon_doe",
        "subject": "hiking",
    }

    post2 = {
        "title": "My favorite recipes",
        "user_name": "jon_doe",
        "subject": "cooking",
    }

    post3 = {
        "title": "I love hiking!",
        "user_name": "jane_doe",
        "subject": "hiking",
    }

    table.put_item(Item=post1)
    table.put_item(Item=post2)
    table.put_item(Item=post3)


def query_data_with_lsi(*, table):
    return table.query(
        IndexName="user_name_subject",
        KeyConditionExpression=Key("user_name").eq("jon_doe")
        & Key("subject").eq("hiking"),
    )["Items"]


@pytest.mark.skip
def test_query_data_with_gsi(posts_table):
    create_posts(table=posts_table)
    resp = query_data_with_lsi(table=posts_table)
    print(resp)  # noqa: T001
