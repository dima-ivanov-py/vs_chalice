from uuid import uuid4

BOOKS_TABLE = {
    "env_var": "BOOKS_TABLE_NAME",
    "TableName": f"books-table-{uuid4()}",
    "KeySchema": [
        {"AttributeName": "title", "KeyType": "HASH"},
        {"AttributeName": "author", "KeyType": "RANGE"},
    ],
    "AttributeDefinitions": [
        {"AttributeName": "title", "AttributeType": "S"},
        {"AttributeName": "author", "AttributeType": "S"},
    ],
    "ProvisionedThroughput": {"ReadCapacityUnits": 5, "WriteCapacityUnits": 5},
}
