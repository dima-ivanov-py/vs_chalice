from uuid import uuid4

POSTS_TABLE = {
    "env_var": "POSTS_TABLE_NAME",
    "TableName": f"posts-table-{uuid4()}",
    "KeySchema": [
        {"AttributeName": "user_name", "KeyType": "HASH"},
        {"AttributeName": "title", "KeyType": "RANGE"},
    ],
    "AttributeDefinitions": [
        {"AttributeName": "title", "AttributeType": "S"},
        {"AttributeName": "user_name", "AttributeType": "S"},
        {"AttributeName": "subject", "AttributeType": "S"},
    ],
    "LocalSecondaryIndexes": [
        {
            "IndexName": "user_name_subject",
            "KeySchema": [
                {"AttributeName": "user_name", "KeyType": "HASH"},
                {"AttributeName": "subject", "KeyType": "RANGE"},
            ],
            "Projection": {"ProjectionType": "ALL"},
        }
    ],
    "ProvisionedThroughput": {"ReadCapacityUnits": 5, "WriteCapacityUnits": 5},
}
