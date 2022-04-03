from uuid import uuid4

EMPLOYEES_TABLE = {
    "env_var": "EMPLOYEES_TABLE_NAME",
    "TableName": f"employees-table-{uuid4()}",
    "KeySchema": [{"AttributeName": "emp_id", "KeyType": "HASH"}],
    "AttributeDefinitions": [
        {"AttributeName": "emp_id", "AttributeType": "N"},
        {"AttributeName": "email", "AttributeType": "S"},
    ],
    "GlobalSecondaryIndexes": [
        {
            "IndexName": "email",
            "KeySchema": [{"AttributeName": "email", "KeyType": "HASH"}],
            "Projection": {"ProjectionType": "ALL"},
            "ProvisionedThroughput": {
                "ReadCapacityUnits": 5,
                "WriteCapacityUnits": 5,
            },
        }
    ],
    "ProvisionedThroughput": {"ReadCapacityUnits": 5, "WriteCapacityUnits": 5},
}
