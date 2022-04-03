from uuid import uuid4

USERS_TABLE = {
    "env_var": "USERS_TABLE_NAME",
    "TableName": f"users-table-{uuid4()}",
    "KeySchema": [{"AttributeName": "username", "KeyType": "HASH"}],
    "AttributeDefinitions": [
        {"AttributeName": "username", "AttributeType": "S"}
    ],
    "ProvisionedThroughput": {"ReadCapacityUnits": 5, "WriteCapacityUnits": 5},
}
