from boto3.dynamodb.conditions import Key
from chalicelib.config import PAGINATION_LIMIT


def _response(*, table, username, uid, forward=True):
    return table.query(
        KeyConditionExpression=Key("username").eq(username),
        ExclusiveStartKey={"username": username, "uid": uid},
        ScanIndexForward=forward,
        Limit=PAGINATION_LIMIT,
    )["Items"]


def list_items_selector(*, table, username, next_=None, back=None):
    if next_:
        return _response(table=table, username=username, uid=next_)

    if back:
        return _response(
            table=table, username=username, uid=back, forward=False
        )

    return table.query(
        KeyConditionExpression=Key("username").eq(username),
        Limit=PAGINATION_LIMIT,
    )["Items"]
