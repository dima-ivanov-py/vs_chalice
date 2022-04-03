from decimal import Decimal
from uuid import uuid4

import pytest
from boto3.dynamodb.conditions import Key
from chalicelib.selectors.get_product import get_product_selector
from chalicelib.services.products.create_product import CreateProductService


@pytest.mark.skip
def test_test(products_table):
    print(products_table.table_status)  # noqa
    print("-" * 79)  # noqa
    print(products_table.scan()["Items"])  # noqa
    print("-" * 79)  # noqa
    product_1 = {
        "title": str(uuid4()),
        "price": "100.22",
        "username": str(uuid4()),
        "uid": str(uuid4()),
    }
    create_service = CreateProductService(table=products_table, data=product_1)
    create_service()
    products_table.wait_until_exists(product_1)
    print(products_table.scan()["Items"])  # noqa
    print("-" * 79)  # noqa
    product_2 = {
        "title": str(uuid4()),
        "price": "100.22",
        "username": str(uuid4()),
        "uid": str(uuid4()),
    }
    create_service.set_data(data=product_2)
    create_service()
    print(products_table.scan()["Items"])  # noqa
    print("-" * 79)  # noqa
    a_product = get_product_selector(
        table=products_table,
        username=product_1["username"],
        uid=product_1["uid"],
    )
    print(a_product)  # noqa
    print("-" * 79)  # noqa
    a_product = products_table.query(
        IndexName="price",
        KeyConditionExpression=Key("price").eq(Decimal("100.22")),
    )["Items"]
    print(a_product)  # noqa
