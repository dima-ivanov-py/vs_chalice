import json
from typing import Any, Dict

from chalicelib.services.products.create_product import CreateProductService


class TestCreateProductAPI:
    @staticmethod
    def run_test(
        *,
        token,
        client,
        monkeypatch,
        products_table,
        path: str = "/products",
        headers=None,
        data: Dict[str, Any],
    ):
        def get_test_table(*args, **kwargs):
            return products_table

        monkeypatch.setattr(CreateProductService, "get_table", get_test_table)
        if not headers:
            headers = {
                "Content-Type": "application/json",
                "Authorization": token,
            }

        return client.http.post(
            path=path, headers=headers, body=json.dumps(data)
        )

    def test_add_new_product(
        self, authorized_user_token, client, monkeypatch, products_table
    ):
        response = self.run_test(
            token=authorized_user_token["token"],
            monkeypatch=monkeypatch,
            products_table=products_table,
            client=client,
            data={"title": "a_title", "price": "23.21"},
        )

        assert response.status_code == 201

    def test_price_is_not_decimal(
        self, authorized_user_token, client, monkeypatch, products_table
    ):
        response = self.run_test(
            token=authorized_user_token["token"],
            monkeypatch=monkeypatch,
            products_table=products_table,
            client=client,
            data={"title": "a_title", "price": "aaa"},
        )

        assert response.status_code == 400
