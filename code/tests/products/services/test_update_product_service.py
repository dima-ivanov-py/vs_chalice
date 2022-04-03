from decimal import Decimal

from chalicelib.selectors.get_product import get_product_selector
from chalicelib.services.products.update_product import UpdateProductService


class TestUpdateProductService:
    def test_can_update_product(self, products):
        table = products["table"]
        product = products["products_of_user_3"]["product_0"]
        data = {
            "title": "WOW",
            "price": "777",
            "username": product["username"],
            "uid": product["uid"],
        }
        update_service = UpdateProductService(table=table, data=data)
        result = update_service()
        product = get_product_selector(
            table=table, uid=product["uid"], username=product["username"]
        )
        product["price"] = round(Decimal(float(product["price"])), 2)
        assert product == result

    def test_product_does_not_exist(self, products):
        table = products["table"]
        data = {
            "title": "WOW",
            "price": "777",
            "username": "FAKE_USERNAME",
            "uid": "FAKE_UID",
        }
        update_service = UpdateProductService(table=table, data=data)
        updated = update_service()
        assert updated is None

    def test_set_data(self, products):
        table = products["table"]
        product = products["products_of_user_3"]["product_0"]
        data = {
            "title": "WOW",
            "price": "777",
            "username": product["username"],
            "uid": product["uid"],
        }
        update_service = UpdateProductService(table=table)
        update_service.set_data(data=data)
        result = update_service()
        product = get_product_selector(
            table=table, uid=product["uid"], username=product["username"]
        )
        product["price"] = round(Decimal(float(product["price"])), 2)
        assert product == result
