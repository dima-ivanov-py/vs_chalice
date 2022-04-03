from decimal import Decimal

from chalicelib.config import DEFAULT_USERNAME
from chalicelib.selectors.get_product import get_product_selector
from chalicelib.services.products.create_product import CreateProductService


class TestCreateProductService:
    def test_can_add_and_retrieve_data(self, products_table):
        data = {
            "title": "First item",
            "price": "234.23",
            "username": DEFAULT_USERNAME,
            "uid": "saldfk23",
        }
        service = CreateProductService(table=products_table, data=data)
        product_id = service()["uid"]
        must_contain = {"title": "First item", "price": Decimal("234.23")}
        full_record = get_product_selector(
            table=products_table, uid=product_id, username=DEFAULT_USERNAME
        )
        assert dict(full_record, **must_contain) == full_record
