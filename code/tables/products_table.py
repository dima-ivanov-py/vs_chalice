from uuid import uuid4

PRODUCTS_TABLE = {
    "env_var": "PRODUCTS_TABLE_NAME",
    "TableName": f"products-table-{uuid4()}",
    "KeySchema": [
        {"AttributeName": "username", "KeyType": "HASH"},
        {"AttributeName": "uid", "KeyType": "RANGE"},
    ],
    "AttributeDefinitions": [
        {"AttributeName": "username", "AttributeType": "S"},
        {"AttributeName": "uid", "AttributeType": "S"},
        {"AttributeName": "price", "AttributeType": "N"},
    ],
    "GlobalSecondaryIndexes": [
        {
            "IndexName": "price",
            "KeySchema": [{"AttributeName": "price", "KeyType": "HASH"}],
            "Projection": {"ProjectionType": "ALL"},
            "ProvisionedThroughput": {
                "ReadCapacityUnits": 5,
                "WriteCapacityUnits": 5,
            },
        }
    ],
    "ProvisionedThroughput": {"ReadCapacityUnits": 5, "WriteCapacityUnits": 5},
}
