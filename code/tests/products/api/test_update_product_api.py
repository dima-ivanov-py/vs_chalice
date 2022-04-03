import json
from typing import Any, Dict

from chalicelib.services.products.update_product import UpdateProductService


class TestUpdateProductAPI:
    @staticmethod
    def run_test(
        *,
        token,
        client,
        mocker,
        monkeypatch,
        product,
        table,
        path: str = "/products",
        uid: str,
        headers=None,
        data: Dict[str, Any],
    ):
        def get_test_table(*args, **kwargs):
            return table

        monkeypatch.setattr(UpdateProductService, "get_table", get_test_table)
        mocker.patch(
            "chalicelib.controllers.products.get_authorized_username",
            return_value=product["username"],
        )

        if not headers:
            headers = {
                "Content-Type": "application/json",
                "Authorization": token,
            }

        return client.http.put(
            path=f"{path}/{uid}", headers=headers, body=json.dumps(data)
        )

    def test_can_update_product(
        self, authorized_user_token, client, mocker, monkeypatch, products
    ):
        table = products["table"]
        product = products["products_of_user_1"]["product_0"]
        data = {"title": "a_title", "price": "23.21"}

        response = self.run_test(
            token=authorized_user_token["token"],
            client=client,
            data=data,
            uid=product["uid"],
            mocker=mocker,
            monkeypatch=monkeypatch,
            product=product,
            table=table,
        )

        data["price"] = float(data["price"])

        assert response.status_code == 200
        assert response.json_body == dict(product, **data)

    def test_can_update_product_price(
        self, authorized_user_token, client, mocker, monkeypatch, products
    ):
        table = products["table"]
        product = products["products_of_user_1"]["product_0"]
        data = {"price": "776.22"}
        response = self.run_test(
            token=authorized_user_token["token"],
            client=client,
            data=data,
            uid=product["uid"],
            mocker=mocker,
            monkeypatch=monkeypatch,
            product=product,
            table=table,
        )

        assert response.status_code == 200
        assert response.json_body["price"] == float(data["price"])

    def test_can_update_product_title(
        self, authorized_user_token, client, mocker, monkeypatch, products
    ):
        table = products["table"]
        product = products["products_of_user_1"]["product_0"]
        data = {"title": "NEW_TITLE"}
        response = self.run_test(
            token=authorized_user_token["token"],
            client=client,
            data=data,
            uid=product["uid"],
            mocker=mocker,
            monkeypatch=monkeypatch,
            product=product,
            table=table,
        )

        assert response.status_code == 200
        assert response.json_body["title"] == "NEW_TITLE"

    def test_wrong_product_uid(
        self, authorized_user_token, client, mocker, monkeypatch, products
    ):
        table = products["table"]
        product = products["products_of_user_1"]["product_0"]
        data = {"title": "a_title", "price": "23.21"}
        response = self.run_test(
            token=authorized_user_token["token"],
            client=client,
            data=data,
            uid="WRONG_UID",
            mocker=mocker,
            monkeypatch=monkeypatch,
            product=product,
            table=table,
        )

        assert response.status_code == 404
        assert response.json_body is None

    def test_wrong_price_type(
        self, authorized_user_token, client, mocker, monkeypatch, products
    ):
        table = products["table"]
        product = products["products_of_user_1"]["product_0"]
        data = {"title": "a_title", "price": "WRONG_TYPE"}
        response = self.run_test(
            token=authorized_user_token["token"],
            client=client,
            data=data,
            uid=product["uid"],
            mocker=mocker,
            monkeypatch=monkeypatch,
            product=product,
            table=table,
        )

        assert response.status_code == 400
