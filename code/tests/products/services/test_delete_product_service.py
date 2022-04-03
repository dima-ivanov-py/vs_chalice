import pytest
from chalicelib.selectors.get_product import get_product_selector
from chalicelib.services.products.delete_product import DeleteProductService


class TestDeleteProductService:
    def test_can_delete_product(self, products, products_table):
        table = products["table"]
        product = products["products_of_user_1"]["product_0"]
        delete_service = DeleteProductService(
            table=products_table,
            uid=product["uid"],
            username=product["username"],
        )
        deleted = delete_service()
        with pytest.raises(KeyError):
            get_product_selector(
                table=table, uid=product["uid"], username=product["username"]
            )
        assert deleted is True

    def test_product_does_not_exist(self, products_table):
        delete_service = DeleteProductService(
            table=products_table, uid="FAKE_UID", username="FAKE_USERNAME"
        )
        deleted = delete_service()
        assert deleted is False

    def test_set_uid(self, products, products_table):
        table = products["table"]
        product = products["products_of_user_1"]["product_0"]
        delete_service = DeleteProductService(
            table=products_table, username=product["username"]
        )
        delete_service.set_uid(uid=product["uid"])
        deleted = delete_service()
        with pytest.raises(KeyError):
            get_product_selector(
                table=table, uid=product["uid"], username=product["username"]
            )
        assert deleted is True

    def test_set_username(self, products, products_table):
        table = products["table"]
        product = products["products_of_user_1"]["product_0"]
        delete_service = DeleteProductService(
            uid=product["uid"], table=products_table
        )
        delete_service.set_username(username=product["username"])
        deleted = delete_service()
        with pytest.raises(KeyError):
            get_product_selector(
                table=table, uid=product["uid"], username=product["username"]
            )
        assert deleted is True
