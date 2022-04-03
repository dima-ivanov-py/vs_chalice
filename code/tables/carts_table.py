from uuid import uuid4

CARTS_TABLE = {
    "env_var": "CARTS_TABLE_NAME",
    "TableName": f"carts-table-{uuid4()}",
    "KeySchema": [{"AttributeName": "username", "KeyType": "HASH"}],
    "AttributeDefinitions": [
        {"AttributeName": "username", "AttributeType": "S"}
    ],
    "ProvisionedThroughput": {"ReadCapacityUnits": 5, "WriteCapacityUnits": 5},
}
