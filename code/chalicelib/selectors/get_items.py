from boto3.dynamodb.conditions import Key


def get_items_by_username(table, username):
    return table.query(KeyConditionExpression=Key("username").eq(username))[
        "Items"
    ]
