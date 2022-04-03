from uuid import uuid4

ORDERS_TABLE = {
    "env_var": "ORDERS_TABLE_NAME",
    "TableName": f"orders-table-{uuid4()}",
    "KeySchema": [
        {"AttributeName": "username", "KeyType": "HASH"},
        {"AttributeName": "uid", "KeyType": "RANGE"},
    ],
    "AttributeDefinitions": [
        {"AttributeName": "username", "AttributeType": "S"},
        {"AttributeName": "uid", "AttributeType": "S"},
        {"AttributeName": "status", "AttributeType": "S"},
        {"AttributeName": "product_username", "AttributeType": "S"},
        {"AttributeName": "product_uid", "AttributeType": "S"},
        {"AttributeName": "amount", "AttributeType": "N"},
    ],
    "ProvisionedThroughput": {"ReadCapacityUnits": 1, "WriteCapacityUnits": 1},
    "LocalSecondaryIndexes": [
        {
            "IndexName": "username_status",
            "KeySchema": [
                {"AttributeName": "username", "KeyType": "HASH"},
                {"AttributeName": "status", "KeyType": "RANGE"},
            ],
            "Projection": {"ProjectionType": "ALL"},
        },
        {
            "IndexName": "username_product_username",
            "KeySchema": [
                {"AttributeName": "username", "KeyType": "HASH"},
                {"AttributeName": "product_username", "KeyType": "RANGE"},
            ],
            "Projection": {"ProjectionType": "ALL"},
        },
        {
            "IndexName": "username_product_uid",
            "KeySchema": [
                {"AttributeName": "username", "KeyType": "HASH"},
                {"AttributeName": "product_uid", "KeyType": "RANGE"},
            ],
            "Projection": {"ProjectionType": "ALL"},
        },
        {
            "IndexName": "username_amount",
            "KeySchema": [
                {"AttributeName": "username", "KeyType": "HASH"},
                {"AttributeName": "amount", "KeyType": "RANGE"},
            ],
            "Projection": {"ProjectionType": "ALL"},
        },
    ],
}
